import time
import matplotlib.pyplot as plt
import sys
import copy


def get_valid_n():
    """获取用户输入的有效N值"""
    while True:
        try:
            n = int(input("请输入一个大于等于4的整数N: "))
            if n < 4:
                print("输入错误：N必须大于等于4，请重新输入。")
            else:
                return n
        except ValueError:
            print("输入错误：请输入一个有效的整数。")


def is_safe(board, row, col, n):
    """检查在(row, col)位置放置皇后是否安全"""
    # 检查列冲突
    for i in range(row):
        if board[i][col] == 1:
            return False

    # 检查左上对角线
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # 检查右上对角线
    for i, j in zip(range(row, -1, -1), range(col, n)):
        if board[i][j] == 1:
            return False

    return True


def apply_symmetry(solution, n, symmetry_type):
    """对解应用对称变换"""
    new_solution = copy.deepcopy(solution)

    if symmetry_type == "horizontal":
        # 水平对称（左右翻转）
        for i in range(n):
            new_solution[i] = new_solution[i][::-1]

    elif symmetry_type == "vertical":
        # 垂直对称（上下翻转）
        new_solution = new_solution[::-1]

    elif symmetry_type == "diagonal":
        # 主对角线对称（左上到右下）
        for i in range(n):
            for j in range(i + 1, n):
                new_solution[i][j], new_solution[j][i] = new_solution[j][i], new_solution[i][j]

    elif symmetry_type == "anti_diagonal":
        # 副对角线对称（右上到左下）
        for i in range(n):
            for j in range(n - i - 1):
                new_solution[i][j], new_solution[n - j - 1][n - i - 1] = \
                    new_solution[n - j - 1][n - i - 1], new_solution[i][j]

    elif symmetry_type == "rotate_90":
        # 顺时针旋转90度
        new_solution = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_solution[j][n - i - 1] = solution[i][j]

    elif symmetry_type == "rotate_180":
        # 顺时针旋转180度
        new_solution = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_solution[n - i - 1][n - j - 1] = solution[i][j]

    elif symmetry_type == "rotate_270":
        # 顺时针旋转270度（或逆时针旋转90度）
        new_solution = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_solution[n - j - 1][i] = solution[i][j]

    return new_solution


def is_unique(solution, existing_solutions, n):
    """检查解是否唯一（考虑对称性）"""
    if not existing_solutions:
        return True

    # 生成当前解的所有对称变换
    symmetries = [
        solution,
        apply_symmetry(solution, n, "horizontal"),
        apply_symmetry(solution, n, "vertical"),
        apply_symmetry(solution, n, "diagonal"),
        apply_symmetry(solution, n, "anti_diagonal"),
        apply_symmetry(solution, n, "rotate_90"),
        apply_symmetry(solution, n, "rotate_180"),
        apply_symmetry(solution, n, "rotate_270")
    ]

    # 检查是否与现有解重复
    for sym in symmetries:
        for existing in existing_solutions:
            if sym == existing:
                return False

    return True


def backtrack_with_symmetry(board, row, n, solutions, find_all=True, start_col=0):
    """带对称性剪枝的回溯法求解N皇后问题"""
    if row == n:
        # 找到一个基础解
        solution = []
        for i in range(n):
            row_data = []
            for j in range(n):
                row_data.append(board[i][j])
            solution.append(row_data)

        # 检查解是否唯一（考虑对称性）
        if is_unique(solution, solutions, n):
            solutions.append(solution)
            return True if not find_all else False
        return False

    found = False
    # 对第一行特殊处理，只搜索到(n+1)//2列，利用对称性
    end_col = (n + 1) // 2 if row == 0 else n
    for col in range(start_col, end_col):
        if is_safe(board, row, col, n):
            board[row][col] = 1
            if backtrack_with_symmetry(board, row + 1, n, solutions, find_all, 0):
                found = True
                if not find_all:
                    return True
            board[row][col] = 0

    return found


def solve_n_queens(n, find_all=True):
    """求解N皇后问题的主函数"""
    board = [[0 for _ in range(n)] for _ in range(n)]
    solutions = []

    # 特殊处理：当n=2或3时无解，但题目中已确保n≥4
    if n < 4:
        return solutions

    # 只在第一行应用对称性剪枝，后续行搜索全部列
    backtrack_with_symmetry(board, 0, n, solutions, find_all, 0)

    # 如果只需要一个解，直接返回
    if not find_all and solutions:
        return [solutions[0]]

    # 如果需要所有解，通过对称变换生成其他解
    if find_all and len(solutions) > 0:
        original_solutions = solutions.copy()
        solutions = []

        # 记录已添加的解，避免重复
        unique_solutions = set()

        for sol in original_solutions:
            # 添加基础解
            sol_tuple = tuple(tuple(row) for row in sol)
            if sol_tuple not in unique_solutions:
                solutions.append(sol)
                unique_solutions.add(sol_tuple)

            # 应用各种对称变换生成新解
            symmetries = [
                ("horizontal", apply_symmetry(sol, n, "horizontal")),
                ("vertical", apply_symmetry(sol, n, "vertical")),
                ("diagonal", apply_symmetry(sol, n, "diagonal")),
                ("anti_diagonal", apply_symmetry(sol, n, "anti_diagonal")),
                ("rotate_90", apply_symmetry(sol, n, "rotate_90")),
                ("rotate_180", apply_symmetry(sol, n, "rotate_180")),
                ("rotate_270", apply_symmetry(sol, n, "rotate_270"))
            ]

            for name, sym in symmetries:
                sym_tuple = tuple(tuple(row) for row in sym)
                if sym_tuple not in unique_solutions:
                    solutions.append(sym)
                    unique_solutions.add(sym_tuple)

    return solutions


def print_board(board):
    """打印棋盘布局"""
    for row in board:
        for cell in row:
            print('Q' if cell == 1 else '.', end=' ')
        print()
    print()


def analyze_performance():
    """分析算法性能"""
    try:
        print("\n正在分析算法性能...")
        times = []
        ns = list(range(4, 13))

        for n in ns:
            start_time = time.time()
            solve_n_queens(n)
            end_time = time.time()
            elapsed_time = end_time - start_time
            times.append(elapsed_time)
            print(f"N={n}, 耗时: {elapsed_time:.6f}秒")

        # 绘制性能曲线
        plt.figure(figsize=(10, 6))
        plt.plot(ns, times, 'o-')
        plt.title('带对称性剪枝的N皇后问题算法性能分析')
        plt.xlabel('N')
        plt.ylabel('运行时间(秒)')
        plt.grid(True)
        plt.savefig('n_queens_performance_symmetry.png')
        print("性能分析图表已保存为n_queens_performance_symmetry.png")
    except ImportError:
        print("性能分析图表功能需要matplotlib库，请安装后再使用")


def main():
    """主函数"""
    n = get_valid_n()

    while True:
        choice = input("请选择输出方式 (1-所有解, 2-仅一个解, 3-性能分析, q-退出): ").strip().lower()

        if choice == '1':
            print(f"\n正在寻找N={n}的所有解...")
            start_time = time.time()
            solutions = solve_n_queens(n, find_all=True)
            end_time = time.time()

            if solutions:
                print(f"找到{len(solutions)}个解:")
                for i, sol in enumerate(solutions):
                    print(f"解 {i + 1}:")
                    print_board(sol)
            else:
                print(f"未找到解（这是不可能的，因为N≥4时一定有解）")

            print(f"计算耗时: {end_time - start_time:.6f}秒")

        elif choice == '2':
            print(f"\n正在寻找N={n}的一个解...")
            start_time = time.time()
            solutions = solve_n_queens(n, find_all=False)
            end_time = time.time()

            if solutions:
                print(f"找到一个解:")
                print_board(solutions[0])
            else:
                print(f"未找到解（这是不可能的，因为N≥4时一定有解）")

            print(f"计算耗时: {end_time - start_time:.6f}秒")

        elif choice == '3':
            analyze_performance()

        elif choice == 'q':
            print("程序已退出。")
            sys.exit()

        else:
            print("无效选择，请重新输入。")


if __name__ == "__main__":
    main()