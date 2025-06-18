import time
from typing import List, Tuple


def is_safe(row: int, col: int, cols: set, diag1: set, diag2: set) -> bool:
    """检查当前位置是否安全"""
    return col not in cols and (row - col) not in diag1 and (row + col) not in diag2


def solve_n_queens(n: int, find_all: bool = True) -> Tuple[List[List[str]], int]:
    """解决N皇后问题"""
    solutions = []
    current = [-1] * n

    def backtrack(row: int) -> None:
        """回溯函数"""
        if row == n:
            # 解压缩为棋盘布局
            board = []
            for col in current:
                board.append('.' * col + 'Q' + '.' * (n - col - 1))
            solutions.append(board)
            return

        for col in range(n):
            if is_safe(row, col, cols, diag1, diag2):
                # 放置皇后
                current[row] = col
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)

                # 递归到下一行
                backtrack(row + 1)

                # 回溯（找到单个解时终止）
                if solutions and not find_all:
                    return

                # 移除皇后
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)

    # 初始化回溯过程
    cols, diag1, diag2 = set(), set(), set()
    backtrack(0)
    return solutions, len(solutions)


def main():
    """主函数"""
    while True:
        try:
            n = int(input("请输入棋盘大小 N (≥4): "))
            if n >= 4:
                break
            print("错误：N 必须 ≥4")
        except ValueError:
            print("错误：请输入整数")

    mode = input("输出所有解? (y/n): ").lower()
    find_all = True if mode == 'y' else False

    start_time = time.time()
    solutions, count = solve_n_queens(n, find_all)
    elapsed = time.time() - start_time

    print(f"\n找到 {count} 个解 (耗时: {elapsed:.4f}秒)\n")

    # 打印解
    max_display = 10  # 最多显示的解法数量
    if solutions:
        if not find_all:
            print(f"解法 1:\n" + "\n".join(solutions[0]) + "\n")
        else:
            for i, sol in enumerate(solutions[:max_display], 1):
                print(f"解法 {i}:\n" + "\n".join(sol) + "\n")
            if count > max_display:
                print(f"显示前{max_display}个解（共{count}个）")


if __name__ == "__main__":
    main()