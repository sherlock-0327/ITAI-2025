
def is_safe(board, row, col, n):
    # 检查当前列是否有其他皇后
    for i in range(row):
        if board[i][col] == 1:
            return False

    # 检查左上对角线是否有其他皇后
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # 检查右上对角线是否有其他皇后
    for i, j in zip(range(row, -1, -1), range(col, n)):
        if board[i][j] == 1:
            return False

    return True

def solve_n_queens_util(board, row, n, solutions, single_solution=False):
    # 如果已经放置完所有行，则找到一个解
    if row >= n:
        solutions.append([row[:] for row in board])
        if single_solution:
            return True
        return False

    res = False
    for i in range(n):
        if is_safe(board, row, i, n):
            board[row][i] = 1  # 放置皇后
            if solve_n_queens_util(board, row + 1, n, solutions, single_solution):
                res = True
            board[row][i] = 0  # 移除皇后（回溯）

    return res

def solve_n_queens(n, single_solution=False):
    # 检查输入是否合法
    if n < 4:
        print("N必须至少为4")
        return [], 0

    board = [[0 for _ in range(n)] for _ in range(n)]  # 初始化棋盘
    solutions = []
    solve_n_queens_util(board, 0, n, solutions, single_solution)

    return solutions, len(solutions)

def print_board(board):
    # 打印棋盘布局
    for row in board:
        print(" ".join("Q" if x else "-" for x in row))
    print()

def main():
    try:
        n = int(input("请输入棋盘大小（N ≥ 4）："))
    except ValueError:
        print("无效输入。请输入一个整数。")
        return

    if n < 4:
        print("N必须至少为4。")
        return

    choice = input("是否只需要一个解？(y/n): ").strip().lower()
    single_solution = choice == 'y'

    solutions, total_solutions = solve_n_queens(n, single_solution)
    if total_solutions == 0:
        print(f"N={n}时没有解")
    elif single_solution:
        print(f"N={n}的一个可能解:")
        print_board(solutions[0])
    else:
        print(f"N={n}的所有{total_solutions}个解:")
        for idx, solution in enumerate(solutions, start=1):
            print(f"解 {idx}:")
            print_board(solution)

if __name__ == "__main__":
    main()



