import time
import matplotlib.pyplot as plt
import numpy as np
import sys

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 黑体# 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class NQueensSolver:
    def __init__(self):
        self.solutions = []  # 存储所有解
        self.board = []  # 当前棋盘状态
        self.n = 0  # 棋盘大小
        self.start_time = 0  # 记录开始时间

    def is_valid(self, row, col):
        """检查在(row, col)位置放置皇后是否合法"""
        # 检查列冲突
        for i in range(row):
            if self.board[i] == col:
                return False

        # 检查左上对角线
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if self.board[i] == j:
                return False

        # 检查右上对角线
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, self.n)):
            if self.board[i] == j:
                return False

        return True

    def backtrack(self, row):
        """回溯算法核心函数"""
        # 如果已经放置了n个皇后，找到一个解
        if row == self.n:
            self.solutions.append(self.board.copy())
            return

        # 尝试在当前行的每一列放置皇后
        for col in range(self.n):
            if self.is_valid(row, col):
                self.board[row] = col
                self.backtrack(row + 1)
                # 回溯：撤销选择
                self.board[row] = -1

    def solve(self, n, find_all=True):
        """求解N皇后问题"""
        self.n = n
        self.board = [-1] * n
        self.solutions = []
        self.start_time = time.time()

        self.backtrack(0)

        elapsed_time = time.time() - self.start_time
        return elapsed_time

    def print_solution(self, solution):
        """打印一个解的棋盘布局"""
        for row in range(self.n):
            line = ['Q' if col == solution[row] else '.' for col in range(self.n)]
            print(' '.join(line))
        print()

    def print_all_solutions(self):
        """打印所有解"""
        print(f"找到 {len(self.solutions)} 个解:")
        for i, solution in enumerate(self.solutions):
            print(f"解 {i + 1}:")
            self.print_solution(solution)

    def run_experiment(self, min_n=4, max_n=12):
        """运行实验并绘制时间增长曲线"""
        times = []
        n_values = list(range(min_n, max_n + 1))

        print("运行实验...")
        for n in n_values:
            print(f"求解 {n} 皇后问题...")
            time_taken = self.solve(n)
            times.append(time_taken)
            print(f"{n} 皇后问题: {len(self.solutions)} 个解, 用时 {time_taken:.4f} 秒")

        # 绘制时间增长曲线
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, times, 'o-', linewidth=2)
        plt.xlabel('N (棋盘大小)')  # 横坐标
        plt.ylabel('运行时间 (秒)')  # 纵坐标
        plt.title('N皇后问题求解时间')  # 图表标题
        plt.grid(True)
        plt.savefig('n_queens_time.png')
        plt.show()

        # 计算理论时间复杂度 (近似值)
        theoretical_times = [n ** n / 1e10 for n in n_values]  # 简化的理论复杂度
        theoretical_times = [t / max(theoretical_times) * max(times) for t in theoretical_times]

        # 绘制理论与实际对比
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, times, 'o-', linewidth=2, label='实际时间')
        plt.plot(n_values, theoretical_times, 's--', linewidth=2, label='理论时间 (近似)')
        plt.xlabel('N (棋盘大小)')  # 横坐标
        plt.ylabel('相对时间')  # 纵坐标
        plt.title('N皇后问题: 实际与理论时间对比')  # 图表标题
        plt.legend()
        plt.grid(True)
        plt.savefig('n_queens_comparison.png')
        plt.show()


def main():
    solver = NQueensSolver()

    # 获取用户输入
    while True:
        try:
            n = int(input("请输入棋盘大小 N (N ≥ 4): "))
            if n < 4:
                print("N 必须大于等于 4，请重新输入。")
                continue
            break
        except ValueError:
            print("输入无效，请输入一个整数。")

    find_all = input("是否找出所有解? (y/n, 默认 y): ").lower() != 'n'

    # 求解问题
    time_taken = solver.solve(n, find_all)

    # 输出结果
    print(f"\n求解完成! 用时: {time_taken:.4f} 秒")
    print(f"找到 {len(solver.solutions)} 个解")

    if len(solver.solutions) > 0:
        if find_all:
            solver.print_all_solutions()
        else:
            print("第一个解:")
            solver.print_solution(solver.solutions[0])

    # 运行实验
    run_exp = input("\n是否运行实验 (计算 N=4 到 N=12 的时间)? (y/n, 默认 n): ").lower() == 'y'
    if run_exp:
        solver.run_experiment()


if __name__ == "__main__":
    main()

