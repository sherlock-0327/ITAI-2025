# N-Queens Problem Solver with Bitwise Optimization and Backtracking (English comments and prompts)

import time
import matplotlib.pyplot as plt

def solve_n_queens_backtracking(n: int, find_all: bool = True):
    """
    Backtracking solver for N-Queens.
    Arguments:
        n         -- size of the board (number of queens)
        find_all  -- if True, find all solutions; if False, stop after first solution
    Returns:
        List of solutions, each represented as a list of column indices per row
    """
    solutions = []
    cols = set()    # occupied columns
    diag1 = set()   # occupied main diagonals (r - c)
    diag2 = set()   # occupied anti-diagonals (r + c)
    board = [-1] * n

    def backtrack(r: int) -> bool:
        """Place queen on row r."""
        if r == n:
            solutions.append(board.copy())
            return True
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            # place queen
            cols.add(c); diag1.add(r - c); diag2.add(r + c)
            board[r] = c

            found = backtrack(r + 1)

            # remove queen (backtrack)
            cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)
            if found and not find_all:
                return True
        return False

    backtrack(0)
    return solutions

def total_n_queens_bit(n: int) -> int:
    """
    Bitwise optimized solver for counting N-Queens solutions.
    Uses bit masks and symmetry pruning.
    Returns total count of distinct solutions.
    """
    all_ones = (1 << n) - 1

    def backtrack(cols: int, diag1: int, diag2: int) -> int:
        if cols == all_ones:
            return 1
        count = 0
        # compute available positions
        available = ~(cols | diag1 | diag2) & all_ones
        while available:
            bit = available & -available
            available -= bit
            count += backtrack(
                cols | bit,
                (diag1 | bit) << 1,
                (diag2 | bit) >> 1
            )
        return count

    count = 0
    half = n // 2
    # symmetry pruning: only place first queen in left half, then double count
    for i in range(half):
        bit = 1 << i
        count += backtrack(bit, bit << 1, bit >> 1)
    count *= 2
    # if n is odd, handle the middle column
    if n % 2:
        i = half
        bit = 1 << i
        count += backtrack(bit, bit << 1, bit >> 1)
    return count

def format_solution(sol):
    """
    Convert a solution (column list) into a visual board representation.
    """
    n = len(sol)
    return ["." * sol[r] + "Q" + "." * (n - sol[r] - 1) for r in range(n)]

def main():
    # prompt for board size
    while True:
        try:
            n = int(input("Enter number of queens N (N >= 4): "))
            if n < 4:
                print("N must be at least 4. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # choose mode
    mode = input("Choose mode: (1) print solutions, (2) count only: ").strip()
    if mode == '1':
        find_all = input("Find all solutions? (y/n): ").strip().lower() == 'y'
        solutions = solve_n_queens_backtracking(n, find_all)
        total = len(solutions)
        if total == 0:
            print("No solutions found.")
        else:
            if not find_all:
                print("Displaying one solution:")
                solutions = solutions[:1]
            else:
                print(f"Total solutions found: {total}")
            for idx, sol in enumerate(solutions, start=1):
                print(f"Solution #{idx}:")
                for row in format_solution(sol):
                    print(row)
                print()
    else:
        total = total_n_queens_bit(n)
        print(f"Total number of solutions (bitwise optimized): {total}")

    # benchmark bitwise count from N=4 to N=12
    Ns = list(range(4, 13))
    times = []
    print("\nBenchmarking bitwise count approach for N = 4 to 12:")
    for n_ex in Ns:
        start = time.time()
        total_n_queens_bit(n_ex)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"N={n_ex}, Time={elapsed:.6f} s")

    # plot performance curve
    plt.figure()
    plt.plot(Ns, times, marker='o')
    plt.xlabel("N")
    plt.ylabel("Elapsed Time (s)")
    plt.title("Bitwise N-Queens Counting Performance (N=4–12)")
    plt.show()

if __name__ == "__main__":
    main()
