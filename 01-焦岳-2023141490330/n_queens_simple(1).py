
# 文件名: n_queens_simple.py
# 描述: 简化版 N 皇后问题求解器，使用回溯法和 O(1) 冲突检测

def solve_n_queens(n, find_all=True):
    solutions = []
    board = [-1] * n
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)
    diag2 = [False] * (2 * n - 1)

    def is_safe(row, col):
        return not cols[col] and not diag1[row - col + n - 1] and not diag2[row + col]

    def place_queen(row, col):
        board[row] = col
        cols[col] = diag1[row - col + n - 1] = diag2[row + col] = True

    def remove_queen(row, col):
        board[row] = -1
        cols[col] = diag1[row - col + n - 1] = diag2[row + col] = False

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return not find_all
        for col in range(n):
            if is_safe(row, col):
                place_queen(row, col)
                if backtrack(row + 1):
                    return True
                remove_queen(row, col)
        return False

    backtrack(0)
    return solutions

def print_solutions(solutions, n):
    print(f"N={n} 共找到 {len(solutions)} 个解\n" + "-"*20)
    for i, sol in enumerate(solutions):
        print(f"解 {i+1}:")
        for row in range(n):
            print(" ".join("Q" if sol[row] == col else "." for col in range(n)))
        print()

if __name__ == "__main__":
    while True:
        try:
            n = input("请输入N (>=4), 或输入 q 退出: ")
            if n.lower() == 'q':
                break
            n = int(n)
            if n < 4:
                print("请输入大于等于4的整数")
                continue
            find_all = input("查找所有解？(Y/N): ").strip().upper() != 'N'
            solutions = solve_n_queens(n, find_all)
            print_solutions(solutions, n)
        except:
            print("输入无效，请重试。")
