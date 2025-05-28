import time
import matplotlib.pyplot as plt
from typing import List, Tuple, Set
import sys


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class NQueensSolver:
    """N皇后问题求解器"""

    def __init__(self, n: int):
        """
        初始化N皇后求解器

        Args:
            n: 棋盘大小和皇后数量
        """
        if n < 4:
            raise ValueError("N必须大于等于4")

        self.n = n
        self.solutions = []
        self.solution_count = 0

        # 优化：使用集合快速检查冲突
        self.cols = set()  # 已占用的列
        self.diag1 = set()  # 主对角线 (row - col)
        self.diag2 = set()  # 副对角线 (row + col)

    def is_safe(self, row: int, col: int) -> bool:
        """
        检查在(row, col)位置放置皇后是否安全

        Args:
            row: 行索引
            col: 列索引

        Returns:
            bool: 是否安全
        """
        return (col not in self.cols and
                (row - col) not in self.diag1 and
                (row + col) not in self.diag2)

    def place_queen(self, row: int, col: int):
        """放置皇后并更新冲突集合"""
        self.cols.add(col)
        self.diag1.add(row - col)
        self.diag2.add(row + col)

    def remove_queen(self, row: int, col: int):
        """移除皇后并更新冲突集合"""
        self.cols.remove(col)
        self.diag1.remove(row - col)
        self.diag2.remove(row + col)

    def backtrack(self, row: int, board: List[int], find_all: bool = True) -> bool:
        """
        回溯算法求解N皇后问题

        Args:
            row: 当前处理的行
            board: 当前棋盘状态，board[i]表示第i行皇后所在的列
            find_all: 是否查找所有解

        Returns:
            bool: 是否找到解
        """
        if row == self.n:
            # 找到一个解
            self.solutions.append(board[:])
            self.solution_count += 1
            return not find_all  # 如果只要一个解，返回True停止搜索

        for col in range(self.n):
            if self.is_safe(row, col):
                # 放置皇后
                board[row] = col
                self.place_queen(row, col)

                # 递归搜索下一行
                if self.backtrack(row + 1, board, find_all):
                    return True

                # 回溯：移除皇后
                self.remove_queen(row, col)

        return False

    def solve(self, find_all: bool = True) -> Tuple[List[List[int]], int]:
        """
        求解N皇后问题

        Args:
            find_all: 是否查找所有解

        Returns:
            tuple: (解的列表, 解的数量)
        """
        self.solutions = []
        self.solution_count = 0
        self.cols.clear()
        self.diag1.clear()
        self.diag2.clear()

        board = [-1] * self.n
        start_time = time.time()

        self.backtrack(0, board, find_all)

        end_time = time.time()
        self.solve_time = end_time - start_time

        return self.solutions, self.solution_count

    def print_board(self, solution: List[int]):
        """
        打印棋盘

        Args:
            solution: 一个解，solution[i]表示第i行皇后所在的列
        """
        print(f"\n{self.n}×{self.n} 棋盘解:")
        print("  " + " ".join([f"{i:2d}" for i in range(self.n)]))

        for row in range(self.n):
            print(f"{row:2d}", end=" ")
            for col in range(self.n):
                if solution[row] == col:
                    print("♛ ", end=" ")
                else:
                    print("· ", end=" ")
            print()

    def print_all_solutions(self):
        """打印所有解"""
        if not self.solutions:
            print("没有找到解")
            return

        print(f"\n找到 {self.solution_count} 个解:")

        for i, solution in enumerate(self.solutions):
            print(f"\n=== 解 {i + 1} ===")
            self.print_board(solution)


def get_valid_input() -> int:
    """
    获取有效的N值输入

    Returns:
        int: 有效的N值
    """
    while True:
        try:
            n = int(input("请输入N的值 (N >= 4): "))
            if n < 4:
                print("错误: N必须大于等于4，请重新输入")
                continue
            return n
        except ValueError:
            print("错误: 请输入一个有效的整数")
        except KeyboardInterrupt:
            print("\n程序已退出")
            sys.exit(0)


def performance_analysis():
    """性能分析：测试不同N值的运行时间"""
    print("\n=== 性能分析 ===")
    print("测试N=4到N=12的运行时间...")

    n_values = list(range(4, 13))
    times = []
    solution_counts = []

    for n in n_values:
        print(f"测试 N={n}...", end=" ")

        solver = NQueensSolver(n)
        start_time = time.perf_counter()
        solutions, count = solver.solve(find_all=True)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        solution_counts.append(count)

        print(f"用时: {elapsed_time:.4f}秒, 解的数量: {count}")

    # 绘制时间增长曲线
    try:
        plt.figure(figsize=(12, 5))

        # 时间增长曲线
        plt.subplot(1, 2, 1)
        plt.plot(n_values, times, 'bo-', linewidth=2, markersize=6)
        plt.xlabel('N (棋盘大小)')
        plt.ylabel('运行时间 (秒)')
        plt.title('N皇后问题运行时间增长曲线')
        plt.grid(True, alpha=0.3)
        plt.yscale('log')  # 使用对数刻度

        # 解的数量增长曲线
        plt.subplot(1, 2, 2)
        plt.plot(n_values, solution_counts, 'ro-', linewidth=2, markersize=6)
        plt.xlabel('N (棋盘大小)')
        plt.ylabel('解的数量')
        plt.title('N皇后问题解的数量增长曲线')
        plt.grid(True, alpha=0.3)
        plt.yscale('log')  # 使用对数刻度

        plt.tight_layout()
        plt.show()

    except ImportError:
        print("注意: matplotlib未安装，无法显示图表")

    # 打印详细结果表格
    print("\n详细结果表格:")
    print(f"{'N':>3} | {'解的数量':>8} | {'运行时间(秒)':>12} | {'时间增长比':>10}")
    print("-" * 45)

    prev_time = None
    for i, (n, count, t) in enumerate(zip(n_values, solution_counts, times)):
        if prev_time is not None and prev_time > 0:
            growth_ratio = t / prev_time
            print(f"{n:>3} | {count:>8} | {t:>12.6f} | {growth_ratio:>10.2f}x")
        else:
            print(f"{n:>3} | {count:>8} | {t:>12.6f} | {'---':>10}")
        prev_time = t


def main():
    """主程序"""
    print("=" * 50)
    print("           N皇后问题求解器")
    print("=" * 50)

    while True:
        try:
            print("\n请选择操作:")
            print("1. 求解N皇后问题")
            print("2. 性能分析 (N=4到N=12)")
            print("3. 退出")

            choice = input("\n请输入选择 (1-3): ").strip()

            if choice == "1":
                n = get_valid_input()

                print("\n请选择求解模式:")
                print("1. 找到所有解")
                print("2. 只找一个解")

                mode_choice = input("请输入选择 (1-2): ").strip()
                find_all = mode_choice != "2"

                print(f"\n开始求解 {n}×{n} 棋盘的N皇后问题...")

                solver = NQueensSolver(n)
                start_time = time.perf_counter()
                solutions, count = solver.solve(find_all)
                end_time = time.perf_counter()

                elapsed_time = end_time - start_time

                if count > 0:
                    print(f"\n求解完成! 用时: {elapsed_time:.4f}秒")

                    if find_all:
                        print(f"总共找到 {count} 个解")

                        if count <= 10:  # 如果解的数量不多，显示所有解
                            show_all = input("\n是否显示所有解? (y/n): ").strip().lower()
                            if show_all == 'y':
                                solver.print_all_solutions()
                        else:
                            print(f"解的数量较多({count}个)，是否显示前5个解?")
                            show_some = input("(y/n): ").strip().lower()
                            if show_some == 'y':
                                for i in range(min(5, count)):
                                    print(f"\n=== 解 {i + 1} ===")
                                    solver.print_board(solutions[i])
                    else:
                        print("找到一个解:")
                        solver.print_board(solutions[0])
                else:
                    print(f"没有找到解 (用时: {elapsed_time:.4f}秒)")

            elif choice == "2":
                performance_analysis()

            elif choice == "3":
                print("感谢使用，再见!")
                break

            else:
                print("无效选择，请重新输入")

        except KeyboardInterrupt:
            print("\n\n程序已退出")
            break
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
    