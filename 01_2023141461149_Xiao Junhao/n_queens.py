import time
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  
matplotlib.rcParams['axes.unicode_minus'] = False #图表正常中文显示

class Solution:
    def solveNQueens(self, n):
        result = []#列表存储结果
        cols = set()
        pos_diag = set()  
        neg_diag = set()  
        board = [['.' for _ in range(n)] for _ in range(n)]
        def backtrack(row):
            if row == n:
                solution = [''.join(row) for row in board]
                result.append(solution)
                return
            if row == 0 and n > 1:
                col_range = range((n + 1) // 2) if n % 2 == 1 else range(n // 2)
            else:
                col_range = range(n)
            
            for col in col_range:
                if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                    continue
                board[row][col] = 'Q'
                cols.add(col)
                pos_diag.add(row + col)
                neg_diag.add(row - col)
                backtrack(row + 1)
                board[row][col] = '.'
                cols.remove(col)
                pos_diag.remove(row + col)
                neg_diag.remove(row - col)
            if row == 0 and n > 1 and result:
                original_count = len(result)
                for i in range(original_count):
                    mirror_solution = []
                    for row_str in result[i]:
                        mirror_row = row_str[::-1]  # 反转字符串
                        mirror_solution.append(mirror_row)
                    if n % 2 == 1 and result[i][0][(n-1)//2] == 'Q':
                        continue 
                    if mirror_solution not in result: 
                        result.append(mirror_solution)
        backtrack(0)
        return result
    
    def printSolution(self, solutions):
        for i, solution in enumerate(solutions):
            print(f"解决方案 {i+1}:")
            for row in solution:
                print(row)
            print()
    
    def countAttackingPairs(self, board, n):
        attacking_pairs = 0
        queens = []
        # 找出所有皇后的位置
        for i in range(n):
            for j in range(n):
                if board[i][j] == 'Q':
                    queens.append((i, j))
        # 检查每对皇后是否互相攻击
        for i in range(len(queens)):
            for j in range(i+1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                if r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2):
                    attacking_pairs += 1
        return attacking_pairs


if __name__ == "__main__":
    sol = Solution()
    while True:
        try:
            n = int(input("请输入N的值（棋盘大小和皇后数量，N>=4）: "))
            if n >= 4:
                break
            else:
                print("非法输入警告：N必须大于或等于4。请重新输入。")
        except ValueError:
            print("非法输入警告：请输入一个整数。请重新输入。")
    start_time = time.time()
    solutions = sol.solveNQueens(n)
    end_time = time.time()
    print(f"N = {n} 时共有 {len(solutions)} 种解决方案。")
    print(f"计算耗时: {end_time - start_time:.4f} 秒")
    # 增强的用户交互
    if solutions:
        print("\n请选择输出方式:")
        print("1. 只显示一个解决方案")
        print("2. 显示所有解决方案")
        print("3. 显示指定数量的解决方案")
        print("4. 显示指定索引的解决方案")
        output_choice = int(input("请输入选择 (1-4): "))
        if output_choice == 1:
            print("\n第一个解决方案:")
            for row in solutions[0]:
                print(row)
        elif output_choice == 2:
            print("\n所有解决方案:")
            sol.printSolution(solutions)
        elif output_choice == 3:
            num = int(input(f"请输入要显示的解决方案数量 (1-{len(solutions)}): "))
            num = min(num, len(solutions))
            print(f"\n前 {num} 个解决方案:")
            for i in range(num):
                print(f"解决方案 {i+1}:")
                for row in solutions[i]:
                    print(row)
                print()
        elif output_choice == 4:
            idx = int(input(f"请输入要显示的解决方案索引 (1-{len(solutions)}): "))
            if 1 <= idx <= len(solutions):
                print(f"\n第 {idx} 个解决方案:")
                for row in solutions[idx-1]:
                    print(row)
            else:
                print("索引超出范围！")
        else:
            print("无效选择！")
    else:
        print("没有找到解决方案。")
    print("\n正在记录N=4到N=12的运行时间并绘制时间增长曲线...")
    n_values_for_plot = range(4, 13) # N从4到12
    times = []
    solution_counts = []
    for current_n in n_values_for_plot:
        print(f"计算 N = {current_n} 的解决方案...")
        start_time_plot = time.time()
        current_solutions = sol.solveNQueens(current_n)
        end_time_plot = time.time()
        
        elapsed_time = end_time_plot - start_time_plot
        times.append(elapsed_time)
        solution_counts.append(len(current_solutions))
        print(f"N = {current_n} 耗时: {elapsed_time:.4f} 秒, 找到 {len(current_solutions)} 个解。")
    plt.figure(figsize=(10, 6))
    plt.plot(n_values_for_plot, times, marker='o', linestyle='-', color='b')
    plt.xlabel('N 值 (棋盘大小)')
    plt.ylabel('计算耗时 (秒)')
    plt.title('N皇后问题回溯算法时间增长曲线')
    plt.grid(True)
    plt.xticks(n_values_for_plot)
    plt.tight_layout()
    plt.savefig('n_queens_time_growth.png', dpi=300)
    plt.show()
    # 绘制解决方案曲线
    plt.figure(figsize=(10, 6))
    plt.plot(n_values_for_plot, solution_counts, marker='o', linestyle='-', color='g')
    plt.xlabel('N 值 (棋盘大小)')
    plt.ylabel('解决方案数量')
    plt.title('N皇后问题解决方案数量曲线')
    plt.grid(True)
    plt.xticks(n_values_for_plot)
    plt.tight_layout()
    plt.savefig('n_queens_solution_counts.png', dpi=300)
    plt.show()