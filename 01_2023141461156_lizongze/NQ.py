
import time
import matplotlib.pyplot as plt

def solve_n_queens(n, find_all=True):
    """
    Solve the N-Queens problem using backtracking.
    Args:
        n (int): The size of the board and number of queens.
        find_all (bool): If True, find all solutions; if False, stop after the first solution.
    Returns:
        List[List[int]]: A list of solutions, each represented by a list of column indices.
    """
    solutions = []
    cols = set()  # occupied columns
    diag1 = set()  # occupied main diagonals (r - c)
    diag2 = set()  # occupied anti-diagonals (r + c)
    board = [-1] * n  # board[r] = c indicates a queen at row r, column c

    def backtrack(r):
        if r == n:
            # Found a complete arrangement
            solutions.append(board.copy())
            return True
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            # Place queen
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            board[r] = c

            found = backtrack(r + 1)

            # Remove queen (backtrack)
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
            if found and not find_all:
                # If only one solution is needed, stop here
                return True
        return False

    backtrack(0)
    return solutions


def format_solution(sol):
    """
    Convert a solution (list of column indices) to a visual board representation.
    """
    n = len(sol)
    return ["." * sol[r] + "Q" + "." * (n - sol[r] - 1) for r in range(n)]


def main():
    # 输入处理
    while True:
        try:
            n = int(input("input the number of the queen N（N >= 4）："))
            if n < 4:
                print("N must be over 4，please input again")
            else:
                break
        except ValueError:
            print("please input the valid number(n>=4)")

    # 用户选择输出模式
    choice = input("whether you want to see the all of the possible results(y/n)：").strip().lower()
    find_all = (choice == 'y')

    # 求解
    solutions = solve_n_queens(n, find_all=find_all)
    count = len(solutions)

    # 输出结果
    if count == 0:
        print("no solutions found")
    else:
        if not find_all:
            print("show  one solutions ")
            solutions = solutions[:1]
        else:
            print(f"there are {count} solution(s)")
        for idx, sol in enumerate(solutions, start=1):
            print(f"solution #{idx}:")
            for line in format_solution(sol):
                print(line)
            print()
        if find_all:
            print(f"there are {count} different solution(s)。")

    # 实验分析：记录 N=4 到 N=12 的运行时间
    Ns = list(range(4, 13))
    times = []
    print("\nexperiment analysis:record the time consuming")
    for n_ex in Ns:
        start = time.time()
        solve_n_queens(n_ex, find_all=True)
        duration = time.time() - start
        times.append(duration)
        print(f"N = {n_ex} ：{duration:.4f} seconds")

    # 绘制时间增长曲线
    plt.figure()
    plt.plot(Ns, times)
    plt.xlabel("N")
    plt.ylabel("run time (s)")
    plt.title("N Queens plot:")
    plt.show()


if __name__ == "__main__":
    main()
