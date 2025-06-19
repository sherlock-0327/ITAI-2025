import time
import matplotlib.pyplot as plt

def get_input():
    """获取并验证用户输入"""
    while True:
        try:
            n = int(input("请输入N（N≥4）："))
            if n >= 4:
                return n
            else:
                print("N必须大于等于4，请重新输入。")
        except ValueError:
            print("输入无效，请输入一个整数。")

def print_board(solution, n):
    """打印棋盘布局"""
    for row in range(n):
        line = ['.'] * n
        line[solution[row]] = 'Q'
        print(''.join(line))
    print()

def solve_n_queens(n, find_all=True):
    """
    使用位运算优化的回溯算法解决N皇后问题
    :param n: 棋盘大小
    :param find_all: 是否查找所有解
    :return: 解列表或第一个解
    """
    solutions = []
    cols = 0
    diag1 = 0
    diag2 = 0
    queen_col = [0] * n

    def backtrack(row):
        nonlocal cols, diag1, diag2
        if row == n:
            solutions.append(queen_col.copy())
            if not find_all:
                return False  # 找到第一个解后终止递归
            return True
        
        for col in range(n):
            d1 = row + col
            d2 = row - col + n - 1
            if not (cols & (1 << col)) and not (diag1 & (1 << d1)) and not (diag2 & (1 << d2)):
                # 更新状态掩码
                queen_col[row] = col
                cols ^= (1 << col)
                diag1 ^= (1 << d1)
                diag2 ^= (1 << d2)
                
                if not backtrack(row + 1):
                    return False  # 找到第一个解后终止
                
                # 回溯状态掩码
                cols ^= (1 << col)
                diag1 ^= (1 << d1)
                diag2 ^= (1 << d2)
        return find_all

    backtrack(0)
    return solutions if find_all else solutions[0] if solutions else None

def analyze_time_complexity():
    """分析不同N值下的运行时间"""
    times = {}
    for n in range(4, 13):
        start_time = time.time()
        solve_n_queens(n, find_all=True)
        elapsed_time = time.time() - start_time
        times[n] = elapsed_time
        print(f"N={n} 完成，耗时：{elapsed_time:.6f}秒")
    
    # 绘制时间增长曲线
    plt.plot(list(times.keys()), list(times.values()), marker='o')
    plt.xlabel('N')
    plt.ylabel('运行时间（秒）')
    plt.title('N皇后问题时间复杂度分析')
    plt.savefig('time_complexity.png')
    plt.close()

if __name__ == "__main__":
    n = get_input()
    
    # 用户选择输出模式
    mode = input("选择输出模式（1-所有解，2-仅一个解）：")
    while mode not in ['1', '2']:
        print("输入无效，请重新选择。")
        mode = input("选择输出模式（1-所有解，2-仅一个解）：")
    
    # 解决并输出结果
    start_time = time.time()
    if mode == '1':
        solutions = solve_n_queens(n, find_all=True)
        print(f"总共有 {len(solutions)} 个解。")
        for sol in solutions:
            print_board(sol, n)
    else:
        solution = solve_n_queens(n, find_all=False)
        if solution:
            print("找到一个解：")
            print_board(solution, n)
        else:
            print("无解。")
    
    print(f"运行时间：{time.time() - start_time:.6f}秒")
    
    # 实验分析（可选）
    analyze = input("是否进行时间复杂度分析？（y/n）：")
    if analyze.lower() == 'y':
        analyze_time_complexity()
        print("时间复杂度分析完成，结果已保存为 time_complexity.png")