import time
import matplotlib.pyplot as plt


class NQueensSolver:
    def __init__(self):
        self.solutions = []
        self.time_records = {}

    def is_safe(self, board, row, col):
        """检查当前位置是否安全"""
        # 检查同一列
        for i in range(row):
            if board[i] == col:
                return False
        # 检查左上对角线
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if board[i] == j:
                return False

        # 检查右上对角线
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, len(board))):
            if board[i] == j:
                return False

        return True

    def solve(self, n, all_solutions=True):
        """回溯法求解N皇后问题"""
        self.solutions = []
        board = [-1] * n

        def backtrack(row):
            if row == n:
                self.solutions.append(board[:])
                return

            for col in range(n):
                if self.is_safe(board, row, col):
                    board[row] = col
                    backtrack(row + 1)
                    board[row] = -1
                    if not all_solutions and self.solutions:
                        return

        backtrack(0)
        return self.solutions

    def print_solution(self, solution):
        """打印棋盘布局"""
        n = len(solution)
        for row in range(n):
            line = ""
            for col in range(n):
                line += "Q " if solution[row] == col else ". "
            print(line)
        print()

    def run_experiments(self):
        """运行实验并记录时间"""
        n_values = list(range(4, 13))
        times = []

        for n in n_values:
            start_time = time.time()
            self.solve(n)
            elapsed = time.time() - start_time
            self.time_records[n] = elapsed
            times.append(elapsed)
            print(f"N={n}: {len(self.solutions)} solutions, Time: {elapsed:.6f}s")

        # 绘制时间曲线
        plt.plot(n_values, times, 'o-')
        plt.xlabel('Board Size (N)')
        plt.ylabel('Time (seconds)')
        plt.title('N-Queens Problem Solving Time')
        plt.grid(True)
        plt.savefig('n_queens_time.png')
        plt.show()


def main():
    solver = NQueensSolver()

    # 处理输入
    n = 0
    while n < 4:
        try:
            n = int(input("Enter board size N (N>=4): "))
            if n < 4:
                print("N must be at least 4. Try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # 选择求解模式
    mode = input("Find all solutions? (y/n): ").lower()
    all_solutions = mode == 'y'

    # 求解并输出
    solutions = solver.solve(n, all_solutions)
    print(f"\nFound {len(solutions)} solution(s)\n")

    if all_solutions:
        for idx, sol in enumerate(solutions, 1):
            print(f"Solution {idx}:")
            solver.print_solution(sol)
    elif solutions:
        print("First solution:")
        solver.print_solution(solutions[0])

    # 运行实验分析
    if input("Run performance experiments? (y/n): ").lower() == 'y':
        solver.run_experiments()


if __name__ == "__main__":
    main()