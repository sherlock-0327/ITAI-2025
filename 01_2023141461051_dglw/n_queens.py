import time
import sys

# board: 当前棋盘状态
# row: 当前行
# col: 当前列
# n: 棋盘大小
# 检查在当前行放置皇后是否冲突
def is_valid(board, row, col, n):

    # 检查列
    for i in range(row):
        if board[i][col] == 1:
            return False
    # 检查左上对角线
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1
    # 检查右上对角线
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1
    return True

#solutions: 存放所有解的列表
# 基本回溯法 未使用剪枝优化，主函数使用的是优化后的 这是一开始我所调用的,在这里并未使用，
def solve_n_queens_util(board, row, n, solutions):

    if row == n:
        solution = []
        for i in range(n):
            row_str = ""
            for j in range(n):
                if board[i][j] == 1: # 设置为皇后
                    row_str += "Q"
                else: #其他
                    row_str += "_"
            solution.append(row_str)
        solutions.append(solution)
        return
    for col in range(n):
        if is_valid(board, row, col, n):
            board[row][col] = 1
            solve_n_queens_util(board, row + 1, n, solutions)
            board[row][col] = 0 #回溯


def solve_n_queens(n):

    board = [[0] * n for _ in range(n)]
    solutions = []
    solve_n_queens_util(board, 0, n, solutions)
    return solutions


# 处理输入
def get_valid_input():

    while True:
        try:
            n = int(input("请输入N值（N≥4，输入0退出）: "))
            if n == 0:
                print("退出程序")
                sys.exit(0)
            if n < 4:
                print("N值必须大于等于4，请重新输入。")
            else:
                return n
        except ValueError:
            print("输入无效，请输入一个整数。")


# 打印棋盘布局
def print_solution(solution):

    for row in solution:
        print(row)


# 回溯基础上增加剪枝优化
def solve_n_queens_with_pruning(n):

    if n == 0:
        return []

    solutions = []
    board = [-1] * n  # 使用一维数组存储皇后位置

    def backtrack(row, cols, diag1, diag2):

       #row: 当前处理的行
       #cols: 列约束的位掩码
       #diag1: 主对角线约束的位掩码
       #diag2: 副对角线约束的位掩码
        if row == n:
            solution = []
            for col in board:
                solution.append('_' * col + 'Q' + '_' * (n - col - 1))
            solutions.append(solution)
            return

        # 生成所有可用列的掩码
        available = ((1 << n) - 1) & (~(cols | diag1 | diag2))

        # 处理第一行时利用对称性剪枝
        if row == 0:
            # 只处理前半部分列，后半部分由对称性生成
            limit = (1 << (n // 2)) - 1
            available &= limit

        while available:
            # 获取最低位的1（表示最右侧可用列）
            p = available & -available
            col = bin(p - 1).count('1')  # 计算列索引

            # 记录皇后位置
            board[row] = col

            # 递归处理下一行，更新约束条件
            backtrack(row + 1,
                      cols | p,
                      (diag1 | p) << 1,
                      (diag2 | p) >> 1)

            # 回溯：清除最低位的1，尝试下一个可用列
            available &= available - 1

    backtrack(0, 0, 0, 0)

    # 处理第一行时使用了对称性剪枝，这里需要生成对称解
    if n > 1:
        # 复制并镜像所有除了中心对称的解
        original_count = len(solutions)
        for i in range(original_count):
            sol = solutions[i]
            # 检查是否是中心对称解
            if n % 2 == 1 and board[0] == n // 2:
                continue
            # 生成镜像解
            mirrored = [row[::-1] for row in sol]
            solutions.append(mirrored)

    return solutions


# 主程序入口
if __name__ == "__main__":
    n = get_valid_input()
    start_time = time.perf_counter()
    solutions = solve_n_queens_with_pruning(n)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time #程序运行时间
    print(f"解的总数: {len(solutions)}")
    choice = input("输入'all'输出所有解，否则输出一个解: ")
    if choice.lower() == "all":
        for i, solution in enumerate(solutions):
            print(f"解 {i + 1}:")
            print_solution(solution)
            print("-" * 20)
    else:
        if solutions:
            print("一个解:")
            print_solution(solutions[0])
    print(f"运行时间: {elapsed_time:.8f} 秒")