import time
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


class NQueensSolver:
    def __init__(self):
        self.n = 0
        self.solutions = []
        self.total_solutions = 0
        self.runtime_data = defaultdict(list)

    def is_safe(self, board, row, col):
        """检查在(row, col)放置皇后是否安全"""
        # 检查同一列
        for i in range(row):
            if board[i][col] == 1:
                return False

        # 检查左上对角线
        i, j = row, col
        while i >= 0 and j >= 0:
            if board[i][j] == 1:
                return False
            i -= 1
            j -= 1

        # 检查右上对角线
        i, j = row, col
        while i >= 0 and j < self.n:
            if board[i][j] == 1:
                return False
            i -= 1
            j += 1

        return True

    def solve_n_queens_util(self, board, row):
        """回溯法工具函数"""
        if row == self.n:
            # 找到解决方案
            solution = []
            for r in board:
                solution.append(tuple(r))
            self.solutions.append(tuple(solution))
            self.total_solutions += 1
            return

        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row][col] = 1
                self.solve_n_queens_util(board, row + 1)
                board[row][col] = 0  # 回溯

    def solve_n_queens(self, n, find_all=True):
        """解决N皇后问题"""
        self.n = n
        self.solutions = []
        self.total_solutions = 0

        # 创建空棋盘
        board = [[0 for _ in range(n)] for _ in range(n)]

        # 记录开始时间
        start_time = time.time()

        # 启动回溯2
        self.solve_n_queens_util(board, 0)

        # 记录运行时间
        elapsed_time = time.time() - start_time

        return elapsed_time

    def print_board(self, board):
        """打印棋盘布局"""
        for row in board:
            line = ""
            for cell in row:
                line += "♛ " if cell == 1 else "□ "
            print(line)
        print()

    def get_user_input(self):
        """获取用户输入"""
        while True:
            try:
                n = int(input("请输入皇后数量N (N≥4): "))
                if n < 4:
                    print("N必须大于等于4，请重新输入。")
                else:
                    break
            except ValueError:
                print("输入无效，请输入一个整数。")

        while True:
            choice = input("请选择输出模式 (1: 所有解, 2: 仅一个解, 3: 仅解的数量): ")
            if choice in ['1', '2', '3']:
                break
            print("输入无效，请选择1、2或3。")

        return n, choice

    def run_analysis(self, max_n=12):
        """运行效率分析"""
        print("\n运行效率分析中...")
        n_values = list(range(4, max_n + 1))
        times = []

        for n in n_values:
            print(f"计算 N={n}...")
            elapsed_time = self.solve_n_queens(n, find_all=True)
            times.append(elapsed_time)
            self.runtime_data[n] = {
                'time': elapsed_time,
                'solutions': self.total_solutions
            }
            print(f"  - 找到 {self.total_solutions} 个解, 耗时: {elapsed_time:.4f} 秒")

        # 绘制时间增长曲线
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, times, 'o-', label='实际运行时间')

        # 拟合指数曲线
        x = np.array(n_values)
        y = np.array(times)
        coeffs = np.polyfit(x, np.log(y), 1)
        exp_fit = np.exp(coeffs[1]) * np.exp(coeffs[0] * x)
        plt.plot(x, exp_fit, 'r--', label=f'指数拟合 (e^{coeffs[0]:.2f}n)')

        plt.title('N皇后问题算法时间复杂度分析')
        plt.xlabel('皇后数量 (N)')
        plt.ylabel('运行时间 (秒)')
        plt.yscale('log')
        plt.grid(True, which="both", ls="-")
        plt.legend()
        plt.savefig('n_queens_time_complexity.png')
        print("\n时间复杂度分析图已保存为 'n_queens_time_complexity.png'")

        # 打印分析结果
        print("\n时间复杂度分析:")
        print("N值 | 解的数量 | 运行时间(秒) | 时间增长率")
        prev_time = 0
        for n in n_values:
            data = self.runtime_data[n]
            growth = data['time'] / prev_time if prev_time > 0 else 0
            print(
                f"{n:2} | {data['solutions']:9} | {data['time']:11.4f} | {growth:.2f}" if n > 4 else f"{n:2} | {data['solutions']:9} | {data['time']:11.4f} | -")
            prev_time = data['time']

        print("\n理论时间复杂度: O(N!) (回溯法)")

    def main(self):
        """主函数"""
        print("=" * 50)
        print("N皇后问题求解器")
        print("=" * 50)

        while True:
            print("\n主菜单:")
            print("1: 求解N皇后问题")
            print("2: 运行效率分析 (N=4到12)")
            print("3: 退出")

            choice = input("请选择: ")

            if choice == '1':
                n, output_mode = self.get_user_input()
                elapsed_time = self.solve_n_queens(n, find_all=(output_mode != '2'))

                if output_mode == '1':  # 所有解
                    print(f"\n找到 {self.total_solutions} 个解:")
                    for idx, solution in enumerate(self.solutions, 1):
                        print(f"\n解 {idx}:")
                        self.print_board(solution)

                elif output_mode == '2':  # 仅一个解
                    if self.solutions:
                        print("\n找到一个解:")
                        self.print_board(self.solutions[0])
                    else:
                        print("\n未找到解")

                else:  # 仅解的数量
                    print(f"\n解的数量: {self.total_solutions}")

                print(f"计算耗时: {elapsed_time:.6f} 秒")

            elif choice == '2':
                self.run_analysis()

            elif choice == '3':
                print("感谢使用N皇后问题求解器，再见!")
                break

            else:
                print("无效选择，请重新输入。")


if __name__ == "__main__":
    solver = NQueensSolver()
    solver.main()