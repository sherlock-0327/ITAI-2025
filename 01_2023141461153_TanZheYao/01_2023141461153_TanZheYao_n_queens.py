import time
import matplotlib.pyplot as plt
from typing import List, Tuple

def is_safe(board: List[int], row: int, col: int) -> bool:
    """
    检查当前位置是否安全，即不与已放置的皇后冲突
    
    参数:
        board: 当前棋盘状态，board[i]表示第i行皇后所在的列
        row: 要检查的行
        col: 要检查的列
    
    返回:
        bool: 如果安全返回True，否则返回False
    """
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_n_queens(n: int, use_symmetry: bool = False, find_all: bool = True) -> Tuple[List[List[int]], int]:
    """
    解决N皇后问题
    
    参数:
        n: 棋盘大小和皇后数量
        use_symmetry: 是否使用对称性剪枝优化
        find_all: 是否查找所有解
    
    返回:
        tuple: (解列表, 解的数量)
    """
    solutions = []
    board = [-1] * n
    
    def backtrack(row: int) -> bool:
        if row == n:
            solutions.append(board.copy())
            return not find_all  # 如果只找一个解，找到后返回True停止搜索
        
        max_col = n
        if use_symmetry and row == 0:  # 第一行且使用对称性剪枝
            max_col = (n + 1) // 2  # 只需要尝试前一半列
        
        for col in range(max_col):
            if is_safe(board, row, col):
                board[row] = col
                if backtrack(row + 1):
                    return True
                board[row] = -1
        return False
    
    backtrack(0)
    
    # 如果使用对称性剪枝，需要添加对称解
    if use_symmetry and n > 1 and find_all:
        # 对于奇数棋盘且第一行皇后不在中间列的情况，需要添加镜像解
        if n % 2 == 1:
            mirror_solutions = []
            for sol in solutions:
                if sol[0] != n // 2:  # 第一行皇后不在中间列
                    mirror_sol = [n - 1 - col for col in sol]
                    mirror_solutions.append(mirror_sol)
            solutions.extend(mirror_solutions)
    
    return solutions, len(solutions)

def print_solution(board: List[int]) -> None:
    """打印单个解的棋盘布局"""
    n = len(board)
    for row in range(n):
        line = "".join("Q " if board[row] == col else ". " for col in range(n))
        print(line)
    print()

def get_valid_input() -> int:
    """获取有效的用户输入"""
    while True:
        try:
            n = int(input("请输入棋盘大小N (N ≥ 4): "))
            if n < 4:
                print("N必须大于或等于4，请重新输入。")
            else:
                return n
        except ValueError:
            print("请输入一个有效的整数。")

def main():
    """主函数，处理用户交互"""
    print("N皇后问题求解器")
    n = get_valid_input()
    
    use_symmetry = input("是否使用对称性剪枝优化? (y/n): ").lower() == 'y'
    find_all = input("查找所有解(a)还是仅一个解(s)? (a/s): ").lower() != 's'
    
    start_time = time.time()
    solutions, count = solve_n_queens(n, use_symmetry, find_all)
    end_time = time.time()
    
    if find_all:
        print(f"\n找到 {count} 个解:")
        for i, sol in enumerate(solutions, 1):
            print(f"解 {i}:")
            print_solution(sol)
    else:
        if solutions:
            print("\n找到一个解:")
            print_solution(solutions[0])
        else:
            print("没有找到解。")
    
    print(f"计算耗时: {end_time - start_time:.4f} 秒")

def benchmark():
    """性能测试函数并绘制时间增长曲线"""
    print("性能测试 (N=4 到 N=12):")
    print("N\t全部解\t对称剪枝解\t全部时间\t对称剪枝时间")
    
    n_values = list(range(4, 13))
    times_normal = []
    times_symmetry = []
    counts_normal = []
    counts_symmetry = []
    
    for n in n_values:
        # 普通回溯
        start = time.time()
        _, count = solve_n_queens(n, False, True)
        end = time.time()
        times_normal.append(end - start)
        counts_normal.append(count)
        
        # 对称剪枝回溯
        start = time.time()
        _, count = solve_n_queens(n, True, True)
        end = time.time()
        times_symmetry.append(end - start)
        counts_symmetry.append(count)
        
        print(f"{n}\t{counts_normal[-1]}\t{counts_symmetry[-1]}\t\t"
              f"{times_normal[-1]:.4f}\t{times_symmetry[-1]:.4f}")
    
    # 绘制时间增长曲线
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(n_values, times_normal, 'bo-', label='Standard Backtracking')
    plt.plot(n_values, times_symmetry, 'ro-', label='Symmetric Pruning')
    plt.xlabel('N (Board Size)')
    plt.ylabel('Time (seconds)')
    plt.title('N-Queens Problem Solving Time Comparison')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(n_values, counts_normal, 'bo-', label='Standard Backtracking')
    plt.plot(n_values, counts_symmetry, 'ro-', label='Symmetric Pruning')
    plt.xlabel('N (Board Size)')
    plt.ylabel('Number of Solutions')
    plt.title('N-Queens Problem Number of Solutions')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
    # 取消下面的注释以运行性能测试
    # benchmark()