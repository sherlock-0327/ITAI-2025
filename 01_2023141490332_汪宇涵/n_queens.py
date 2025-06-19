class NQueensSolver:
    def __init__(self):
        self.solutions = []
        self.solution_count = 0

    def is_valid_position(self, board, row, col, n):
        # 检查列
        for i in range(row):
            if board[i] == col:
                return False
            # 检查对角线
            if abs(board[i] - col) == abs(i - row):
                return False
        return True

    def solve_n_queens_util(self, board, row, n):
        if row == n:
            # 找到一个解
            solution = []
            for i in range(n):
                row_str = ['.'] * n
                row_str[board[i]] = 'Q'
                solution.append(''.join(row_str))
            self.solutions.append(solution)
            self.solution_count += 1
            return

        for col in range(n):
            if self.is_valid_position(board, row, col, n):
                board[row] = col
                self.solve_n_queens_util(board, row + 1, n)
                # 回溯 - 不需要显式重置，因为board会被覆盖

    def solve_n_queens(self, n, find_all=True):
        self.solutions = []
        self.solution_count = 0
        board = [-1] * n  # board[i]表示第i行皇后所在的列

        self.solve_n_queens_util(board, 0, n)

        if find_all:
            return self.solutions
        elif self.solutions:
            return [self.solutions[0]]  # 只返回第一个解
        else:
            return []

    def print_solution(self, solution, n):
        for row in solution:
            print(row)
        print()

    def print_all_solutions(self, solutions, n):
        print(f"共有 {len(solutions)} 种解:")
        for i, solution in enumerate(solutions, 1):
            print(f"解 #{i}:")
            self.print_solution(solution, n)


def get_valid_input():
    """获取有效的用户输入"""
    while True:
        try:
            n = int(input("请输入棋盘大小N (N≥4): "))
            if n >= 4:
                return n
            else:
                print("错误：N必须大于或等于4，请重新输入。")
        except ValueError:
            print("错误：请输入一个有效的整数。")


def main():
    solver = NQueensSolver()
    n = get_valid_input()
    find_all = input("查找所有解吗？(y/n, 默认y): ").lower() != 'n'

    solutions = solver.solve_n_queens(n, find_all)

    if find_all:
        solver.print_all_solutions(solutions, n)
        print(f"总解数: {solver.solution_count}")
    elif solutions:
        print("找到一个解:")
        solver.print_solution(solutions[0], n)
    else:
        print("没有找到解。")


if __name__ == "__main__":
    main()