import time
from collections import defaultdict

# --- 用户输入和文件操作 (与原版相同) ---

def is_valid_n(n):
    """检查N是否为有效的整数"""
    return isinstance(n, int) and n >= 4


def get_user_input():
    """获取用户输入的棋盘大小N"""
    while True:
        try:
            n = int(input("请输入一个大于等于4的整数N: "))
            if is_valid_n(n):
                return n
            else:
                print("错误: N 必须是大于等于4的整数")
        except ValueError:
            print("错误: 请输入合法的整数")


def write_solutions_to_file(solutions, count, execution_time, n, algorithm, filename="n_queens_output.txt"):
    """将结果写入文件"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"算法: {algorithm}\n")
        f.write(f"N = {n}\n")
        f.write(f"总解数: {count}\n")
        f.write(f"运行时间: {execution_time:.6f} 秒\n\n")
        for index, solution in enumerate(solutions, start=1):
            f.write(f"解 {index}:\n")
            for row in solution:
                f.write(row + "\n")
            f.write("\n")


# --- 辅助函数：格式化解 ---
def format_solutions(solutions_indices, n):
    """将存储列索引的解格式化为棋盘字符串"""
    formatted = []
    for sol_indices in solutions_indices:
        solution = []
        for i in range(n):
            row = ['* '] * n
            row[sol_indices[i]] = 'Q  '
            solution.append(''.join(row))
        formatted.append(solution)
    return formatted


# --- 算法1: 标准回溯法 ---
def solve_n_queens_standard(n, output_all=True):
    """
    使用标准回溯法求解N皇后问题。
    通过字典/列表实现 O(1) 的冲突检查。
    """
    solutions = []
    cols = [False] * n
    hill_diagonals = defaultdict(bool)  # 主对角线 (row - col)
    dale_diagonals = defaultdict(bool)  # 副对角线 (row + col)
    queens = [-1] * n  # queens[i] = col 表示第i行的皇后在第j列

    def is_not_under_attack(row, col):
        return not (cols[col] or hill_diagonals[row - col] or dale_diagonals[row + col])

    def place_queen(row, col):
        queens[row] = col
        cols[col] = True
        hill_diagonals[row - col] = True
        dale_diagonals[row + col] = True

    def remove_queen(row, col):
        # 回溯时，只需将 queens[row] 设为-1，其他标记在下次覆盖即可
        queens[row] = -1
        cols[col] = False
        hill_diagonals[row - col] = False
        dale_diagonals[row + col] = False

    def backtrack(row=0):
        for col in range(n):
            if is_not_under_attack(row, col):
                place_queen(row, col)
                if row + 1 == n:
                    solutions.append(list(queens))  # 存储列索引的解
                    if not output_all:
                        return True
                else:
                    found = backtrack(row + 1)
                    if found and not output_all:
                        return True
                remove_queen(row, col)
        return False

    start_time = time.time()
    backtrack()
    end_time = time.time()

    execution_time = end_time - start_time
    formatted_sols = format_solutions(solutions, n)
    return formatted_sols, len(solutions), execution_time


# --- 算法2: 位运算优化回溯法 ---
def solve_n_queens_bitwise(n, output_all=True):
    """
    使用位运算优化的回溯法求解N皇后问题。
    """
    solutions_indices = []
    queens = [-1] * n

    # 'all_ones' 是一个N位的掩码，所有位都是1，代表所有列。 e.g., N=8, all_ones = 0b11111111
    all_ones = (1 << n) - 1

    def backtrack(row, cols_mask, hills_mask, dales_mask):
        # base case: 所有皇后都已放置
        if row == n:
            solutions_indices.append(list(queens))
            return len(solutions_indices) == 1 and not output_all

        # 计算当前行所有可放置皇后的安全位置
        available_spots = all_ones & (~(cols_mask | hills_mask | dales_mask))

        # 遍历所有可用的位置
        while available_spots:
            pos = available_spots & -available_spots

            available_spots -= pos

            col = pos.bit_length() - 1
            queens[row] = col
            if backtrack(row + 1, cols_mask | pos, (hills_mask | pos) >> 1, (dales_mask | pos) << 1):
                return True

        return False
    start_time = time.time()
    backtrack(0, 0, 0, 0)  # 初始状态：row=0，所有掩码都为0
    end_time = time.time()

    execution_time = end_time - start_time
    formatted_sols = format_solutions(solutions_indices, n)
    return formatted_sols, len(solutions_indices), execution_time


def main():
    n = get_user_input()

    # 选择算法
    algo_choice = ''
    while algo_choice not in ['1', '2']:
        algo_choice = input("请选择算法: 1. 标准回溯法 2. 位运算法 (输入1或2): ").strip()

    # 选择输出模式
    mode = input("是否在控制台输出所有解? (输入 Y 输出所有解, 任意其他键仅输出一个解): ").strip().lower()
    output_all_console = (mode == 'y')

    solver_func = None
    algo_name = ""
    if algo_choice == '1':
        solver_func = solve_n_queens_standard
        algo_name = "标准回溯法"
    else:
        solver_func = solve_n_queens_bitwise
        algo_name = "位运算法"

    print(f"\n使用 [{algo_name}] 计算 N = {n} 的问题...")

    # 为了保证计时准确，如果用户只看一个解，我们也只运行一次
    solutions, count, exec_time = solver_func(n, output_all_console)

    # 如果用户只看一个解，但我们需要所有解的总数和时间用于写入文件
    if not output_all_console and count > 0:
        all_solutions, all_count, all_exec_time = solver_func(n, True)
    else:
        all_solutions, all_count, all_exec_time = solutions, count, exec_time

    # 控制台输出
    print()
    if solutions:
        if output_all_console:
            print(f"找到 {count} 个解:")
            for idx, solution in enumerate(solutions, 1):
                print(f"解 {idx}:")
                for row in solution:
                    print(row)
                print()
        else:
            print("其中的一个可行解:")
            for row in solutions[0]:
                print(row)
            print()
    else:
        print("未找到任何解。")

    # 文件输出
    write_solutions_to_file(all_solutions, all_count, all_exec_time, n, algo_name)

    print(f"总解数: {all_count}")
    print(f"运行时间 (找到所有解): {all_exec_time:.6f} 秒")
    print(f"N = {n} 的所有解已经使用 [{algo_name}] 计算并写入文件 'n_queens_output.txt'")


if __name__ == "__main__":
    main()