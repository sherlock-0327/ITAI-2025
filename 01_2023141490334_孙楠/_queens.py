import time
import matplotlib.pyplot as plt

def is_safe(board, row, col):
    """检查当前位置是否安全"""
    # 检查列
    for i in range(row):
        if board[i] == col:
            return False
        # 检查对角线
        if abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_n_queens(n, find_all=True):
    """使用回溯法解决N皇后问题"""
    solutions = []
    board = [-1] * n
    
    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                if solutions and not find_all:
                    return
    
    backtrack(0)
    return solutions

def print_solution(board):
    """打印棋盘布局"""
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            line += "Q " if board[row] == col else ". "
        print(line)
    print()

def main():
    """主函数"""
    n = 0
    while n < 4:
        try:
            n = int(input("请输入棋盘大小N (N≥4): "))
            if n < 4:
                print("输入错误！N必须大于或等于4")
        except ValueError:
            print("请输入有效整数！")
    
    find_all = input("输出所有解？(y/n): ").lower() == 'y'
    
    start_time = time.time()
    solutions = solve_n_queens(n, find_all)
    end_time = time.time()
    
    print(f"\n找到 {len(solutions)} 个解:")
    if n <= 8:  # 仅在小规模时打印所有解
        for i, sol in enumerate(solutions):
            print(f"解 {i+1}:")
            print_solution(sol)
    else:
        print("由于N较大，仅打印第一个解:")
        print_solution(solutions[0])
    
    print(f"计算耗时: {end_time - start_time:.4f}秒")
    
    # 实验分析：N=4到N=12的运行时间
    if input("\n是否运行实验分析？(y/n): ").lower() == 'y':
        times = []
        sizes = list(range(4, 13))
        for size in sizes:
            start = time.time()
            solve_n_queens(size)
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"N={size}: {elapsed:.4f}秒")
        
        plt.plot(sizes, times, 'o-')
        plt.xlabel('Board Size (N)')
        plt.ylabel('Time (seconds)')
        plt.title('N-Queens Problem Time Complexity')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    main()
    




