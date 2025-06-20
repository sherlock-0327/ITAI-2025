import time  # 导入时间模块

def is_safe(queens, row, col):
    # 检查在该位置放置皇后是否安全
    for r in range(row):
        c = queens[r]
        if c == col or abs(c - col) == abs(r - row):  # 检查列冲突和对角线冲突
            return False
    return True

def solve_n_queens(n, find_one=False, optimization='none'):
    """
    N皇后问题求解统一函数，支持两种优化方式
    optimization: 'none'(常规回溯), 'bits'(位运算优化)
    """
    solutions = []
    queens = [-1] * n  # 初始化皇后位置数组
    
    # 1. 常规回溯方法
    def solve_backtrack(row):
        if row == n:  # 找到一个解
            solutions.append(queens[:])
            return not find_one
        for col in range(n):
            if is_safe(queens, row, col):
                queens[row] = col
                if not solve_backtrack(row + 1):
                    return False
        return True
    
    # 2. 位运算优化方法
    def solve_bits(row, cols, ld, rd):
        if row == n:
            solutions.append(queens[:])
            return not find_one
        
        # 所有可能放置皇后的位置 (值为0的位表示可放置)
        available = ~(cols | ld | rd) & ((1 << n) - 1)
        
        while available:
            # 取最低位的1（最右侧可用位置）
            pos = available & -available
            col = bin(pos).count('0') - 1  # 计算列号
            
            queens[row] = col
            # 更新占用情况：列、左对角线(左移)、右对角线(右移)
            if not solve_bits(row + 1, 
                             cols | pos,
                             (ld | pos) << 1, 
                             (rd | pos) >> 1):
                return False
                
            # 清除当前尝试位置，尝试下一个
            available &= ~pos
            
        return True
    
    # 根据优化选项调用不同的求解方法
    if optimization == 'bits':
        solve_bits(0, 0, 0, 0)
    else:  # 默认使用常规回溯
        solve_backtrack(0)
        
    return solutions

def print_board(solution):
    n = len(solution)
    for row in solution:
        line = ['Q' if i == row else '.' for i in range(n)]
        print(' '.join(line))
    print("\n")

def input_n():
    while True:
        try:
            n = int(input("输入一个 N 的值 (N >= 4): "))
            if n >= 4:
                return n
            else:
                print("N 最小是 4.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main():
    n = input_n()
    choice = input("找全部解还是一个解 (all/one): ").strip().lower()
    find_one = choice == 'one'
    
    # 选择是否使用位运算
    opt_choice = input("是否使用位运算 (none/bits): ").strip().lower()
    
    start = time.time()  # 开始计时
    solutions = solve_n_queens(n, find_one, opt_choice)
    end = time.time()  # 结束计时

    for sol in solutions:
        print_board(sol)

    print(f"解的总数: {len(solutions)}")
    print(f"运行时间: {end - start:.4f} seconds")
    
    # 添加执行时间对比
    if n <= 12 and opt_choice != 'none' and not find_one:
        print("\n性能对比:")
        methods = ['none', 'bits']
        for method in methods:
            if method == opt_choice:
                continue
            start = time.time()
            sols = solve_n_queens(n, find_one, method)
            method_time = time.time() - start
            print(f"- {method} 方法: {method_time:.4f} 秒")

if __name__ == "__main__":
    main()
