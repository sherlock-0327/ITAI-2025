Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import time

def is_safe(row, col, cols, diag1, diag2):
    """检查当前位置是否安全"""
    return col not in cols and (row - col) not in diag1 and (row + col) not in diag2

def solve_n_queens(n, find_all=True):
    """求解N皇后问题"""
    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return True if not find_all else False
        
        found = False
...         for col in range(n):
...             if is_safe(row, col, cols, diag1, diag2):
...                 # 放置皇后并记录冲突
...                 board[row] = col
...                 cols.add(col)
...                 diag1.add(row - col)
...                 diag2.add(row + col)
...                 
...                 # 递归下一行
...                 if backtrack(row + 1):
...                     if not find_all:
...                         return True
...                 
...                 # 回溯
...                 cols.remove(col)
...                 diag1.remove(row - col)
...                 diag2.remove(row + col)
...                 if found and not find_all:
...                     break
...         return found
...     
...     solutions = []
...     board = [-1] * n
...     cols = set()
...     diag1 = set()
...     diag2 = set()
...     
...     backtrack(0)
...     return solutions
... 
... def print_solution(solution):
...     """打印棋盘布局"""
...     n = len(solution)
...     for row in solution:
...         line = ['Q' if i == row else '.' for i in range(n)]
...         print(' '.join(line))
...     print()
... 
... def main():
...     """主函数"""
    while True:
        try:
            n = int(input("请输入棋盘大小 N (N≥4): "))
            if n < 4:
                print("N必须大于等于4，请重新输入！")
                continue
            break
        except ValueError:
            print("请输入有效的整数！")
    
    mode = input("输出模式 (1=所有解, 2=仅一个解): ").strip()
    find_all = (mode == '1')
    
    start_time = time.time()
    solutions = solve_n_queens(n, find_all)
    elapsed = time.time() - start_time
    
    print(f"\n找到 {len(solutions)} 个解 (耗时: {elapsed:.4f}秒)\n")
    
    if solutions:
        if not find_all or len(solutions) <= 2:
            for sol in solutions:
                print_solution(sol)
        else:
            print("前2个解示例:")
            for sol in solutions[:2]:
                print_solution(sol)

if __name__ == "__main__":
