"""
N皇后问题求解器
张雄-2023141461071
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Set
import json


class NQueensSolver:
    """N皇后问题求解器"""

    def __init__(self, n: int):
        """初始化求解器"""
        self.n = n  # 棋盘大小和皇后数量
        self.solutions = []  # 存储所有解决方案
        self.solution_count = 0  # 解的数量
        self.call_count = 0  # 递归调用次数统计

    def is_safe(self, board: List[int], row: int, col: int) -> bool:
        """检查在指定位置放置皇后是否安全"""
        # 检查当前行之前的所有行
        for i in range(row):
            # 检查列冲突：若已有皇后在同一列
            if board[i] == col:
                return False
            # 检查对角线冲突：行差与列差的绝对值相等
            if abs(board[i] - col) == abs(i - row):
                return False
        return True

    def is_safe_optimized(self, cols: Set[int], diag1: Set[int], diag2: Set[int], row: int, col: int) -> bool:
        """优化版本的安全检查，使用集合存储已占用的列和对角线"""
        # 检查列、主对角线和反对角线是否已被占用
        return (col not in cols and
                (row - col) not in diag1 and
                (row + col) not in diag2)

    def solve_backtrack_basic(self, find_all: bool = True) -> List[List[int]]:
        """基础回溯算法求解N皇后问题"""
        self.solutions = []  # 重置解列表
        self.solution_count = 0  # 重置解计数
        self.call_count = 0  # 重置调用计数

        def backtrack(board: List[int], row: int):
            """递归回溯函数"""
            self.call_count += 1  # 记录递归调用次数

            if row == self.n:
                # 找到一个完整解，添加到解列表
                self.solutions.append(board[:])
                self.solution_count += 1
                # 如果只需要一个解，返回True停止搜索
                return not find_all

            # 尝试在当前行的每一列放置皇后
            for col in range(self.n):
                if self.is_safe(board, row, col):  # 检查位置安全性
                    board[row] = col  # 放置皇后
                    if backtrack(board, row + 1):  # 递归处理下一行
                        return True
                    # 回溯时无需显式重置，下次循环会覆盖当前位置

            return False

        board = [-1] * self.n  # 初始化棋盘，-1表示未放置皇后
        backtrack(board, 0)  # 从第0行开始回溯
        return self.solutions

    def solve_backtrack_optimized(self, find_all: bool = True) -> List[List[int]]:
        """优化版回溯算法，使用集合加速冲突检测"""
        self.solutions = []  # 重置解列表
        self.solution_count = 0  # 重置解计数
        self.call_count = 0  # 重置调用计数

        def backtrack(board: List[int], row: int, cols: Set[int], diag1: Set[int], diag2: Set[int]):
            """带集合优化的递归回溯函数"""
            self.call_count += 1  # 记录递归调用次数

            if row == self.n:
                # 找到一个完整解，添加到解列表
                self.solutions.append(board[:])
                self.solution_count += 1
                # 如果只需要一个解，返回True停止搜索
                return not find_all

            # 尝试在当前行的每一列放置皇后
            for col in range(self.n):
                if self.is_safe_optimized(cols, diag1, diag2, row, col):  # 检查位置安全性
                    # 放置皇后并更新占用集合
                    board[row] = col
                    cols.add(col)
                    diag1.add(row - col)
                    diag2.add(row + col)

                    if backtrack(board, row + 1, cols, diag1, diag2):  # 递归处理下一行
                        return True

                    # 回溯：移除皇后并恢复占用集合
                    cols.remove(col)
                    diag1.remove(row - col)
                    diag2.remove(row + col)

            return False

        board = [-1] * self.n  # 初始化棋盘
        cols = set()  # 已占用的列集合
        diag1 = set()  # 已占用的主对角线集合 (row - col)
        diag2 = set()  # 已占用的反对角线集合 (row + col)

        backtrack(board, 0, cols, diag1, diag2)  # 从第0行开始回溯
        return self.solutions

    def solve_with_symmetry(self, find_all: bool = True) -> List[List[int]]:
        """利用对称性优化的求解方法"""
        if self.n == 1:
            return [[0]]  # N=1时特殊处理

        self.solutions = []  # 重置解列表
        self.solution_count = 0  # 重置解计数
        self.call_count = 0  # 重置调用计数

        def backtrack(board: List[int], row: int, cols: Set[int], diag1: Set[int], diag2: Set[int]):
            """带对称性优化的递归回溯函数"""
            self.call_count += 1  # 记录递归调用次数

            if row == self.n:
                # 找到一个完整解，添加到解列表
                self.solutions.append(board[:])
                self.solution_count += 1
                # 如果只需要一个解，返回True停止搜索
                return not find_all

            # 第一行只考虑前一半位置，利用左右对称性
            col_range = range(self.n // 2) if row == 0 else range(self.n)

            # 尝试在当前行的有效列范围内放置皇后
            for col in col_range:
                if self.is_safe_optimized(cols, diag1, diag2, row, col):  # 检查位置安全性
                    board[row] = col  # 放置皇后
                    cols.add(col)  # 更新列占用集合
                    diag1.add(row - col)  # 更新主对角线占用集合
                    diag2.add(row + col)  # 更新反对角线占用集合

                    if backtrack(board, row + 1, cols, diag1, diag2):  # 递归处理下一行
                        return True

                    # 回溯：移除皇后并恢复占用集合
                    cols.remove(col)
                    diag1.remove(row - col)
                    diag2.remove(row + col)

            return False

        board = [-1] * self.n  # 初始化棋盘
        cols = set()  # 已占用的列集合
        diag1 = set()  # 已占用的主对角线集合
        diag2 = set()  # 已占用的反对角线集合

        backtrack(board, 0, cols, diag1, diag2)  # 从第0行开始回溯

        # 生成对称解：通过左右镜像生成另一半解
        original_solutions = self.solutions[:]
        for solution in original_solutions:
            mirrored = [self.n - 1 - col for col in solution]  # 生成左右镜像解
            if mirrored not in self.solutions:  # 避免重复添加
                self.solutions.append(mirrored)
                self.solution_count += 1

        return self.solutions


def print_board(solution: List[int], n: int):
    """打印棋盘布局"""
    print("+" + "-" * (2 * n + 1) + "+")  # 打印棋盘顶部边框
    for i in range(n):
        row = "|"  # 初始化当前行字符串
        for j in range(n):
            if solution[i] == j:  # 如果当前位置有皇后
                row += " Q"
            else:  # 否则为空白
                row += " ."
        row += " |"  # 结束当前行
        print(row)  # 打印当前行
    print("+" + "-" * (2 * n + 1) + "+")  # 打印棋盘底部边框
    print()  # 打印空行


def print_solutions(solutions: List[List[int]], n: int, max_display: int = 5):
    """打印所有解决方案"""
    print(f"总共找到 {len(solutions)} 个解")  # 打印解的总数

    if len(solutions) == 0:
        print("没有找到解决方案")  # 处理无解情况
        return

    display_count = min(len(solutions), max_display)  # 计算要显示的解数量
    print(f"显示前 {display_count} 个解：\n")  # 打印提示信息

    # 显示前display_count个解
    for i, solution in enumerate(solutions[:display_count]):
        print(f"解 {i + 1}:")  # 打印解的编号
        print_board(solution, n)  # 打印棋盘布局

    if len(solutions) > max_display:
        # 处理解数量过多的情况
        print(f"... 还有 {len(solutions) - max_display} 个解未显示")


def validate_input(n: int) -> bool:
    """验证输入是否合法"""
    return isinstance(n, int) and n >= 4  # N必须是大于等于4的整数


def get_user_input() -> Tuple[int, bool]:
    """获取用户输入"""
    while True:
        try:
            # 获取棋盘大小N
            n = int(input("请输入棋盘大小N (N >= 4): "))
            if not validate_input(n):
                print("错误：N必须是大于等于4的整数，请重新输入")
                continue
            break
        except ValueError:
            print("错误：请输入一个有效的整数")

    while True:
        # 获取是否查找所有解的选项
        choice = input("是否查找所有解？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            return n, True
        elif choice in ['n', 'no', '否']:
            return n, False
        else:
            print("请输入 y 或 n")


def benchmark_algorithms(max_n: int = 12):
    """性能测试函数"""
    print("开始性能测试...")
    print("=" * 60)

    results = {
        'n_values': [],
        'basic_times': [],
        'optimized_times': [],
        'symmetry_times': [],
        'basic_calls': [],
        'optimized_calls': [],
        'symmetry_calls': [],
        'solution_counts': []
    }

    # 对N从4到max_n进行性能测试
    for n in range(4, max_n + 1):
        print(f"测试 N = {n}...")
        results['n_values'].append(n)  # 记录当前测试的N值

        solver = NQueensSolver(n)  # 创建求解器实例

        # 测试基础回溯算法
        start_time = time.time()
        solver.solve_backtrack_basic(find_all=True)
        basic_time = time.time() - start_time
        basic_calls = solver.call_count

        # 测试优化回溯算法
        start_time = time.time()
        solver.solve_backtrack_optimized(find_all=True)
        optimized_time = time.time() - start_time
        optimized_calls = solver.call_count

        # 测试对称性优化算法
        start_time = time.time()
        solver.solve_with_symmetry(find_all=True)
        symmetry_time = time.time() - start_time
        symmetry_calls = solver.call_count

        # 记录测试结果
        results['basic_times'].append(basic_time)
        results['optimized_times'].append(optimized_time)
        results['symmetry_times'].append(symmetry_time)
        results['basic_calls'].append(basic_calls)
        results['optimized_calls'].append(optimized_calls)
        results['symmetry_calls'].append(symmetry_calls)
        results['solution_counts'].append(solver.solution_count)

        # 打印当前N的测试结果
        print(f"  解的数量: {solver.solution_count}")
        print(f"  基础算法: {basic_time:.4f}s ({basic_calls} 次调用)")
        print(f"  优化算法: {optimized_time:.4f}s ({optimized_calls} 次调用)")
        print(f"  对称优化: {symmetry_time:.4f}s ({symmetry_calls} 次调用)")
        print()

    return results  # 返回测试结果


def plot_performance(results: dict):
    """绘制性能分析图表"""
    plt.figure(figsize=(15, 10))  # 设置图表大小

    # 创建2x2的子图布局
    plt.subplot(2, 2, 1)
    plt.plot(results['n_values'], results['basic_times'], 'o-', label='基础回溯', linewidth=2)
    plt.plot(results['n_values'], results['optimized_times'], 's-', label='优化回溯', linewidth=2)
    plt.plot(results['n_values'], results['symmetry_times'], '^-', label='对称优化', linewidth=2)
    plt.xlabel('N (棋盘大小)')
    plt.ylabel('运行时间 (秒)')
    plt.title('算法运行时间对比')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # 使用对数刻度

    plt.subplot(2, 2, 2)
    plt.plot(results['n_values'], results['basic_calls'], 'o-', label='基础回溯', linewidth=2)
    plt.plot(results['n_values'], results['optimized_calls'], 's-', label='优化回溯', linewidth=2)
    plt.plot(results['n_values'], results['symmetry_calls'], '^-', label='对称优化', linewidth=2)
    plt.xlabel('N (棋盘大小)')
    plt.ylabel('递归调用次数')
    plt.title('递归调用次数对比')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # 使用对数刻度

    plt.subplot(2, 2, 3)
    plt.plot(results['n_values'], results['solution_counts'], 'ro-', linewidth=2, markersize=6)
    plt.xlabel('N (棋盘大小)')
    plt.ylabel('解的数量')
    plt.title('解的数量随N的变化')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # 使用对数刻度

    plt.subplot(2, 2, 4)
    # 计算加速比
    speedup_optimized = np.array(results['basic_times']) / np.array(results['optimized_times'])
    speedup_symmetry = np.array(results['basic_times']) / np.array(results['symmetry_times'])

    plt.plot(results['n_values'], speedup_optimized, 's-', label='优化回溯 vs 基础', linewidth=2)
    plt.plot(results['n_values'], speedup_symmetry, '^-', label='对称优化 vs 基础', linewidth=2)
    plt.xlabel('N (棋盘大小)')
    plt.ylabel('加速比')
    plt.title('算法加速比')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()  # 自动调整子图布局
    plt.show()  # 显示图表


def print_performance_table(results: dict):
    """打印性能对比表格"""
    print("\n" + "=" * 100)
    print("性能分析报告")
    print("=" * 100)

    # 打印表格头部
    header = f"{'N':>3} | {'解数':>6} | {'基础时间':>10} | {'优化时间':>10} | {'对称时间':>10} | {'基础调用':>10} | {'优化调用':>10} | {'对称调用':>10} | {'优化加速比':>10} | {'对称加速比':>10}"
    print(header)
    print("-" * 100)

    # 打印每行数据
    for i, n in enumerate(results['n_values']):
        basic_time = results['basic_times'][i]
        opt_time = results['optimized_times'][i]
        sym_time = results['symmetry_times'][i]
        speedup_opt = basic_time / opt_time if opt_time > 0 else 0
        speedup_sym = basic_time / sym_time if sym_time > 0 else 0

        row = f"{n:>3} | {results['solution_counts'][i]:>6} | {basic_time:>10.4f} | {opt_time:>10.4f} | {sym_time:>10.4f} | {results['basic_calls'][i]:>10} | {results['optimized_calls'][i]:>10} | {results['symmetry_calls'][i]:>10} | {speedup_opt:>10.2f} | {speedup_sym:>10.2f}"
        print(row)


def main():
    """主函数"""
    print("N皇后问题求解器")
    print("=" * 50)

    while True:
        print("\n请选择操作：")
        print("1. 求解指定N的皇后问题")
        print("2. 运行性能测试 (N=4到N=12)")
        print("3. 退出")

        choice = input("请输入选择 (1-3): ").strip()  # 获取用户选择

        if choice == '1':
            n, find_all = get_user_input()  # 获取用户输入的N和是否查找所有解
            print(f"\n开始求解 {n} 皇后问题...")

            solver = NQueensSolver(n)  # 创建求解器实例

            # 使用优化算法求解
            start_time = time.time()
            solutions = solver.solve_backtrack_optimized(find_all=find_all)
            solve_time = time.time() - start_time

            # 打印求解结果
            print(f"求解完成！用时: {solve_time:.4f} 秒")
            print(f"递归调用次数: {solver.call_count}")

            if find_all:
                print_solutions(solutions, n)  # 打印所有解
            else:
                if solutions:
                    print("找到一个解:")
                    print_board(solutions[0], n)  # 打印第一个解
                else:
                    print("没有找到解")

        elif choice == '2':
            print("\n这将测试N=4到N=12的性能，可能需要几分钟时间...")
            confirm = input("确认继续？(y/n): ").lower().strip()  # 确认是否进行性能测试

            if confirm in ['y', 'yes', '是']:
                results = benchmark_algorithms(12)  # 运行性能测试
                print_performance_table(results)  # 打印性能表格

                # 询问是否绘制性能图表
                plot_choice = input("\n是否绘制性能图表？(y/n): ").lower().strip()
                if plot_choice in ['y', 'yes', '是']:
                    plot_performance(results)  # 绘制性能图表

        elif choice == '3':
            print("感谢使用！")  # 退出程序
            break

        else:
            print("无效选择，请重新输入")  # 处理无效选择


if __name__ == "__main__":
    main()