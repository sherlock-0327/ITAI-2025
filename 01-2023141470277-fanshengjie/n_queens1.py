import time
import matplotlib.pyplot as plt
import numpy as np
import sys

# 设置matplotlib的中文字体支持
plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 黑体# 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class NQueensSolver:
    def __init__(self):
        """N皇后问题求解器初始化"""
        self.solutions = []  # 存储所有找到的解，每个解是一个列表，表示每行皇后所在的列
        self.board = []  # 当前棋盘状态，用一维数组表示，board[row]=col表示(row,col)位置有一个皇后
        self.n = 0  # 棋盘大小
        self.start_time = 0  # 记录开始时间，用于计算算法运行时间

    def is_valid(self, row, col):
        """
        检查在(row, col)位置放置皇后是否合法
        由于我们是按行放置皇后，所以只需要检查列冲突和对角线冲突
        """
        # 检查列冲突：当前列是否已有皇后
        for i in range(row):
            if self.board[i] == col:
                return False

        # 检查左上对角线：左上方向是否已有皇后
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if self.board[i] == j:
                return False

        # 检查右上对角线：右上方向是否已有皇后
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, self.n)):
            if self.board[i] == j:
                return False

        return True  # 如果没有冲突，则该位置合法

    def backtrack(self, row):
        """
        回溯算法核心函数
        row: 当前要放置皇后的行
        """
        # 基本情况：如果已经放置了n个皇后（到达第n行），说明找到了一个解
        if row == self.n:
            self.solutions.append(self.board.copy())  # 保存当前解的副本
            return

        # 尝试在当前行的每一列放置皇后
        for col in range(self.n):
            if self.is_valid(row, col):  # 检查当前位置是否合法
                self.board[row] = col  # 在(row, col)位置放置皇后
                self.backtrack(row + 1)  # 递归求解下一行
                # 回溯：撤销选择，尝试下一列
                self.board[row] = -1

    def solve(self, n, find_all=True):
        """
        求解N皇后问题（未剪枝）
        n: 棋盘大小
        find_all: 是否找出所有解，默认为True
        """
        self.n = n
        self.board = [-1] * n  # 初始化棋盘，-1表示该位置没有皇后
        self.solutions = []  # 清空解列表
        self.start_time = time.time()  # 记录开始时间

        self.backtrack(0)  # 从第0行开始求解

        elapsed_time = time.time() - self.start_time  # 计算耗时
        return elapsed_time

    def backtrack_optimized(self, row):
        """
        使用剪枝策略的回溯算法核心函数
        利用棋盘的对称性进行优化，只考虑第一行的前半部分列
        """
        # 基本情况：找到一个解
        if row == self.n:
            self.solutions.append(self.board.copy())
            return

        # 优化：第一行只考虑前半部分列，利用对称性减少计算量
        if row == 0:
            end_col = self.n // 2 if self.n % 2 == 0 else self.n // 2 + 1
            for col in range(end_col):
                if self.is_valid(row, col):
                    self.board[row] = col
                    self.backtrack_optimized(row + 1)
                    self.board[row] = -1
        else:
            # 非第一行，考虑所有列
            for col in range(self.n):
                if self.is_valid(row, col):
                    self.board[row] = col
                    self.backtrack_optimized(row + 1)
                    self.board[row] = -1

    def solve_optimized(self, n, find_all=True):
        """
        求解N皇后问题（使用剪枝策略）
        n: 棋盘大小
        find_all: 是否找出所有解，默认为True
        """
        self.n = n
        self.board = [-1] * n
        self.solutions = []
        self.start_time = time.time()

        self.backtrack_optimized(0)  # 使用优化的回溯算法

        # 处理对称解：根据第一行皇后的位置，生成对应的对称解
        if self.n % 2 == 0:
            # 偶数棋盘：对每个解生成其镜像解
            for solution in self.solutions.copy():
                symmetric_solution = [self.n - 1 - col for col in solution]
                self.solutions.append(symmetric_solution)
        else:
            # 奇数棋盘：需要特殊处理中心列的解
            center_col_solutions = [solution for solution in self.solutions if solution[0] == self.n // 2]
            non_center_col_solutions = [solution for solution in self.solutions if solution[0] != self.n // 2]

            # 非中心列的解需要生成镜像解
            for solution in non_center_col_solutions:
                symmetric_solution = [self.n - 1 - col for col in solution]
                self.solutions.append(symmetric_solution)

        elapsed_time = time.time() - self.start_time
        return elapsed_time

    def print_solution(self, solution):
        """
        打印一个解的棋盘布局
        solution: 一个解，是一个列表，表示每行皇后所在的列
        """
        for row in range(self.n):
            line = ['Q' if col == solution[row] else '.' for col in range(self.n)]
            print(' '.join(line))
        print()

    def print_all_solutions(self):
        """打印所有找到的解"""
        print(f"找到 {len(self.solutions)} 个解:")
        for i, solution in enumerate(self.solutions):
            print(f"解 {i + 1}:")
            self.print_solution(solution)

    def run_experiment(self, min_n=4, max_n=12):
        """
        运行实验并绘制时间增长曲线
        比较剪枝前后算法的性能差异
        """
        times_original = []  # 存储未剪枝算法的运行时间
        times_optimized = []  # 存储剪枝后算法的运行时间
        n_values = list(range(min_n, max_n + 1))  # 测试的棋盘大小范围

        print("运行实验...")
        for n in n_values:
            print(f"求解 {n} 皇后问题（未剪枝）...")
            time_taken_original = self.solve(n)
            times_original.append(time_taken_original)
            print(f"{n} 皇后问题（未剪枝）: {len(self.solutions)} 个解, 用时 {time_taken_original:.4f} 秒")

            print(f"求解 {n} 皇后问题（剪枝后）...")
            time_taken_optimized = self.solve_optimized(n)
            times_optimized.append(time_taken_optimized)
            print(f"{n} 皇后问题（剪枝后）: {len(self.solutions)} 个解, 用时 {time_taken_optimized:.4f} 秒")

        # 绘制时间增长曲线
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, times_original, 'o-', linewidth=2, label='未剪枝')
        plt.plot(n_values, times_optimized, 's--', linewidth=2, label='剪枝后')
        plt.xlabel('N (棋盘大小)')
        plt.ylabel('运行时间 (秒)')
        plt.title('N皇后问题求解时间：剪枝前后对比')
        plt.grid(True)
        plt.legend()
        plt.savefig('n_queens_pruning_comparison.png')  # 保存图表
        plt.show()  # 显示图表


def main():
    """主函数：程序入口点"""
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
