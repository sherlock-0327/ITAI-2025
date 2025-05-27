# n_queens.py

import time
from collections import defaultdict

def is_valid_n(n):
    return isinstance(n, int) and n >= 4

def get_user_input():
    while True:
        try:
            n = int(input("请输入一个大于等于4的整数N: "))
            if is_valid_n(n):
                return n
            else:
                print("错误: N 必须是大于等于4的整数")
        except ValueError:
            print("错误: 请输入合法的整数")

def solve_n_queens(n, output_all=True):

    '''
    solutions: 存储所有可行解, 每个解是一个棋盘的字符串列表
    cols: 用于标记每一列是否已有皇后, True 表示该列已被占用
    hill_diagonals: 用于标记主对角线(左上到右下)是否已有皇后, key 为 (row - col)
    dale_diagonals: 用于标记副对角线(右上到左下)是否已有皇后, key 为 (row + col)
    queens: queens[i] 表示第 i 行皇后所在的列，-1 表示该行还未放置皇后
    '''
        
    # 剪枝：判断当前位置(row, col)是否安全
    def is_not_under_attack(row, col):
        return not (cols[col] or hill_diagonals[row - col] or dale_diagonals[row + col])

    # 放置皇后，并标记列和对角线
    def place_queen(row, col):
        queens[row] = col
        cols[col] = True
        hill_diagonals[row - col] = True
        dale_diagonals[row + col] = True

    # 回溯：移除皇后，并取消标记
    def remove_queen(row, col):
        queens[row] = -1
        cols[col] = False
        hill_diagonals[row - col] = False
        dale_diagonals[row + col] = False

    # 记录当前解
    def add_solution():
        solution = []
        for i in range(n):
            row = ['*  '] * n
            row[queens[i]] = 'Q  '
            solution.append(''.join(row))
        solutions.append(solution)

    # 回溯主逻辑
    def backtrack(row=0):
        for col in range(n):
            # 剪枝：如果当前位置安全才尝试放置皇后
            if is_not_under_attack(row, col):
                place_queen(row, col)
                if row + 1 == n:
                    add_solution()
                    if not output_all:
                        return True  # 只需找到一个解时提前返回
                else:
                    found = backtrack(row + 1)
                    if found and not output_all:
                        return True
                # 回溯：撤销当前选择，尝试下一个位置
                remove_queen(row, col)
        return False

    solutions = []
    cols = [False] * n
    hill_diagonals = defaultdict(bool)
    dale_diagonals = defaultdict(bool)
    queens = [-1] * n

    start_time = time.time()
    backtrack()
    end_time = time.time()

    execution_time = end_time - start_time
    return solutions, len(solutions), execution_time

def write_solutions_to_file(solutions, count, execution_time, n, filename="n_queens_output.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"N = {n}\n")
        f.write(f"总解数: {count}\n")
        f.write(f"运行时间: {execution_time:.6f} 秒\n\n")
        for index, solution in enumerate(solutions, start=1):
            f.write(f"解 {index}:\n")
            for row in solution:
                f.write(row + "\n")
            f.write("\n")

def main():
    n = get_user_input()
    mode = input("是否在控制台输出所有解? 输入 Y 输出所有解, 输入 N 仅输出一个解: ").strip().lower()
    output_all = mode == 'y'

    # 控制台输出根据用户选择，文件始终保存所有解
    solutions, count, exec_time = solve_n_queens(n, output_all)
    all_solutions, all_count, all_exec_time = solve_n_queens(n, True)  # 始终获取所有解用于写文件

    # 控制台输出
    print()
    if output_all:
        for idx, solution in enumerate(solutions, 1):
            print(f"解 {idx}:")
            for row in solution:
                print(row)
            print()
    else:
        if solutions:
            print("其中的一个可行解: ")
            for row in solutions[0]:
                print(row)
            print()
        else:
            print("未找到解")

    # 文件输出
    write_solutions_to_file(all_solutions, all_count, all_exec_time, n)

    print(f"总解数: {all_count}")
    print(f"运行时间: {all_exec_time:.6f} 秒")
    print(f"N = {n} 的所有解已经写入文件 'n_queens_output.txt'")

if __name__ == "__main__":
    main()