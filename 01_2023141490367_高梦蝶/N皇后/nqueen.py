import time
from typing import List

def input_n() -> int:
    while True:
        try:
            n = int(input('请输入皇后数量N(≥4): '))
            if n < 4:
                print('N必须≥4，请重新输入')
            else:
                return n
        except ValueError:
            print('输入无效，请输入整数')

def is_safe(row: int, col: int, queen_rows: List[int]) -> bool:
    # 检查列和对角线冲突
    for r in range(row):
        c = queen_rows[r]
        if c == col or abs(row - r) == abs(col - c):
            return False
    return True

def solve_n_queens(n: int, find_all=True) -> List[List[int]]:
    solutions = []
    queen_rows = [-1] * n

    def backtrack(row):
        if row == n:
            solutions.append(queen_rows.copy())
            return
        
        for col in range(n):
            if is_safe(row, col, queen_rows):
                queen_rows[row] = col
                backtrack(row + 1)
                if not find_all and solutions:
                    return
    
    backtrack(0)
    return solutions

def print_solutions(solutions: List[List[int]], n: int):
    for i, sol in enumerate(solutions, 1):
        print(f'解法{i}:')
        for col in sol:
            print('.' * col + 'Q' + '.' * (n - col -1))
        print()

if __name__ == '__main__':
    n = input_n()
    start = time.time()
    
    mode = input('输出所有解？(y/n): ').lower() == 'y'
    solutions = solve_n_queens(n, find_all=mode)
    
    print(f'\n找到{len(solutions)}个解，耗时{time.time()-start:.3f}秒')
    if solutions:
        if mode:
            print_solutions(solutions, n)
        else:
            print('首个解：')
            print_solutions([solutions[0]], n)