def is_safe(board, row, col):
    """检查给定行和列的位置是否安全"""
    for i in range(row):
        # 检查列和对角线攻击
        if board[i] == col or board[i] - i == col - row or board[i] + i == col + row:
            return False
    return True


def solve_n_queens_util(board, row, n, solutions):
    """回溯法解决 N 皇后问题的辅助函数"""
    if row == n:
        solutions.append(board[:])
        return

    # 对称性优化，限制第一个皇后在左半部分
    limit = n // 2 + (n % 2)
    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col
            solve_n_queens_util(board, row + 1, n, solutions)


def print_board(solution):
    """打印棋盘布局"""
    n = len(solution)
    for i in range(n):
        row = ['Q' if j == solution[i] else '.' for j in range(n)]
        print(' '.join(row))
    print()


def solve_n_queens(n):
    """主函数，解决 N 皇后问题"""
    if n < 4:
        return "N must be at least 4."

    board = [-1] * n
    solutions = []

    solve_n_queens_util(board, 0, n, solutions)

    # 打印所有解决方案
    for sol in solutions:
        print_board(sol)

    # 输出总解的数量
    print(f"Total solutions for N={n}: {len(solutions)}")


if __name__ == "__main__":
    while True:
        try:
            n = int(input("Enter the value of N (N >= 4): "))
            if n < 4:
                print("N must be at least 4. Please try again.")
            else:
                solve_n_queens(n)
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")