def solve_n_queens(n):
    """
    解决N皇后问题，利用回溯法和对称性剪枝。
    
    参数:
        n (int): 棋盘的大小和皇后的数量。
    
    返回:
        list: 所有可能的解，每个解是一个列表，表示每行皇后的位置。
    """
    def is_not_under_attack(row, col):
        """
        检查在(row, col)位置放置皇后是否安全。
        
        参数:
            row (int): 当前行。
            col (int): 当前列。
        
        返回:
            bool: 如果安全返回True，否则返回False。
        """
        for prev_row in range(row):
            prev_col = positions[prev_row]
            # 检查是否在同一列或同一对角线上
            if prev_col == col or abs(prev_col - col) == abs(prev_row - row):
                return False
        return True

    def place_queen(row):
        """
        递归地尝试在每一行放置皇后。
        
        参数:
            row (int): 当前行。
        """
        if row == n:
            # 如果所有行都放置了皇后，保存当前解
            solutions.append(positions[:])
            return
        for col in range(n):
            if is_not_under_attack(row, col):
                # 如果安全，放置皇后并递归到下一行
                positions[row] = col
                place_queen(row + 1)

    def add_symmetric_solutions():
        """
        通过对称变换添加所有对称解。
        """
        for solution in solutions:
            # 生成水平对称解
            symmetric_solution = solution[::-1]
            if symmetric_solution not in solutions:
                solutions.append(symmetric_solution)
            # 生成垂直对称解
            symmetric_solution = [n - 1 - col for col in solution]
            if symmetric_solution not in solutions:
                solutions.append(symmetric_solution)
            # 生成对角线对称解
            symmetric_solution = [n - 1 - row for row, col in enumerate(solution)]
            if symmetric_solution not in solutions:
                solutions.append(symmetric_solution)

    solutions = []
    positions = [-1] * n  # 初始化位置数组，-1表示未放置皇后
    place_queen(0)  # 从第一行开始放置皇后
    add_symmetric_solutions()  # 添加对称解
    return solutions

def print_solutions(solutions):
    """
    打印所有解。
    
    参数:
        solutions (list): 所有可能的解。
    """
    for solution in solutions:
        for row in solution:
            print(' '.join(['Q' if col == row else '.' for col in range(len(solution))]))
        print()

def main():
    """
    主函数，处理用户输入和输出。
    """
    import time
    import matplotlib.pyplot as plt

    while True:
        try:
            n = int(input("Enter the number of queens (N >=4): "))
            if n < 4:
                print("N must be greater than 4. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    print("Calculating solutions...")
    start_time = time.time()
    solutions = solve_n_queens(n)
    end_time = time.time()

    print(f"Found {len(solutions)} solutions for {n}-Queens problem.")
    print(f"Time taken: {end_time - start_time:.4f} seconds")

    choice = input("Print all solutions? (y/n): ")
    if choice.lower() == 'y':
        print_solutions(solutions)

if __name__ == "__main__":
    main()
