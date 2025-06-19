import time
import matplotlib.pyplot as plt
import numpy as np
import sys

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class NQueensSolver:
    def __init__(self):
        self.solutions = []  # 存储所有解
        self.board = []  # 当前棋盘状态
        self.n = 0  # 棋盘大小
        self.start_time = 0  # 记录开始时间

    def is_valid(self, row, col):
        """检查位置 (row, col) 是否合法"""
        for i in range(row):
            if self.board[i] == col or abs(self.board[i] - col) == abs(i - row):
                return False
        return True

    def get_conflict_count(self, row, col):
        """计算当前列的冲突数（启发式评分）"""
        conflict = 0
        for i in range(row):
            if self.board[i] == col or abs(self.board[i] - col) == abs(i - row):
                conflict += 1
        return conflict

    def backtrack(self, row):
        """基础回溯算法（未优化）"""
        if row == self.n:
            self.solutions.append(self.board.copy())
            return
        for col in range(self.n):
            if self.is_valid(row, col):
                self.board[row] = col
                self.backtrack(row + 1)
                self.board[row] = -1

    def backtrack_with_heuristic(self, row):
        """带启发式的回溯算法：优先选择冲突少的列"""
        if row == self.n:
            self.solutions.append(self.board.copy())
            return
        # 计算每列的冲突数，并按冲突数从小到大排序
        cols_with_conflict = [(col, self.get_conflict_count(row, col)) for col in range(self.n)]
        sorted_cols = sorted(cols_with_conflict, key=lambda x: x[1])
        for col, _ in sorted_cols:
            if self.is_valid(row, col):
                self.board[row] = col
                self.backtrack_with_heuristic(row + 1)
                self.board[row] = -1

    def solve_original(self, n):
        """原始回溯算法"""
        self.n = n
        self.board = [-1] * n
        self.solutions = []
        self.start_time = time.time()
        self.backtrack(0)
        return time.time() - self.start_time

    def solve_heuristic(self, n):
        """启发式优化回溯算法"""
        self.n = n
        self.board = [-1] * n
        self.solutions = []
        self.start_time = time.time()
        self.backtrack_with_heuristic(0)
        return time.time() - self.start_time

    def print_solution(self, solution):
        """打印解的棋盘布局"""
        for row in range(self.n):
            line = ['Q' if col == solution[row] else '.' for col in range(self.n)]
            print(' '.join(line))
        print()

    def run_experiment(self, min_n=4, max_n=12):
        """对比原始算法、剪枝算法、启发式算法的时间"""
        times_original = []
        times_heuristic = []
        n_values = list(range(min_n, max_n + 1))

        # 测试原始算法
        print("测试原始回溯算法...")
        for n in n_values:
            time_taken = self.solve_original(n)
            times_original.append(time_taken)
            print(f"N={n}: 解数={len(self.solutions)}, 时间={time_taken:.4f}秒")

        # 测试启发式算法
        print("\n测试启发式优化算法...")
        for n in n_values:
            time_taken = self.solve_heuristic(n)
            times_heuristic.append(time_taken)
            print(f"N={n}: 解数={len(self.solutions)}, 时间={time_taken:.4f}秒")

        # 绘制对比曲线
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, times_original, 'o-', label='原始算法', color='blue')
        plt.plot(n_values, times_heuristic, 's--', label='启发式算法', color='red')
        plt.xlabel('N (棋盘大小)')
        plt.ylabel('运行时间 (秒)')
        plt.title('N皇后问题：原始算法 vs 启发式算法')
        plt.legend()
        plt.grid(True)
        plt.savefig('n_queens_heuristic_comparison.png')
        plt.show()


def main():
    solver = NQueensSolver()
    n = int(input("请输入棋盘大小 N (N≥4): "))

    # 求解并对比
    time_original = solver.solve_original(n)
    time_heuristic = solver.solve_heuristic(n)

    print(f"\n原始算法用时: {time_original:.4f} 秒")
    print(f"启发式算法用时: {time_heuristic:.4f} 秒")
    print(f"解数: {len(solver.solutions)}")

    if len(solver.solutions) > 0:
        print("\n第一个解:")
        solver.print_solution(solver.solutions[0])

    # 运行实验
    run_exp = input("\n是否生成时间对比图表? (y/n): ").lower() == 'y'
    if run_exp:
        solver.run_experiment()


if __name__ == "__main__":
    main()