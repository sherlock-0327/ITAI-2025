def solve_n_queens(n, find_all=True):
    """
    使用回溯法解决N皇后问题

    参数:
        n: 棋盘大小
        find_all: 是否查找所有解(True)或仅一个解(False)

    返回:
        解的列表(每个解是一个棋盘布局)和解的总数
    """

    def is_safe(board, row, col):
        """检查当前位置是否安全"""
        # 检查当前列
        for i in range(row):
            if board[i] == col:
                return False
            # 检查对角线
            if abs(board[i] - col) == abs(i - row):
                return False
        return True

    def backtrack(row):
        """回溯主函数"""
        nonlocal count
        if row == n:
            # 找到一个解
            solution = []
            for i in range(n):
                line = ['.'] * n
                line[board[i]] = 'Q'
                solution.append(''.join(line))
            solutions.append(solution)
            count += 1
            return not find_all  # 如果只找一个解，找到后返回True停止搜索

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                if backtrack(row + 1):
                    return True
                board[row] = -1  # 回溯
        return False

    # 初始化
    board = [-1] * n
    solutions = []
    count = 0

    backtrack(0)
    return solutions, count


def print_solution(solution):
    """打印单个解"""
    for row in solution:
        print(row)
    print()


def main():
    """主函数"""
    while True:
        try:
            n = int(input("请输入棋盘大小N(≥4): "))
            if n < 4:
                print("N必须≥4，请重新输入")
                continue
            break
        except ValueError:
            print("请输入有效的整数")

    while True:
        choice = input("查找所有解(a)还是仅一个解(o)? ").lower()
        if choice in ['a', 'o']:
            find_all = (choice == 'a')
            break
        print("请输入'a'或'o'")

    solutions, count = solve_n_queens(n, find_all)

    if solutions:
        if find_all:
            print(f"\n找到{count}个解:")
            for i, solution in enumerate(solutions, 1):
                print(f"解 {i}:")
                print_solution(solution)
        else:
            print("\n找到一个解:")
            print_solution(solutions[0])
    else:
        print("未找到解")


if __name__ == "__main__":
    main()