import time
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'SimHei'

def test_runtime(n_min=4, n_max=12):
    ns = []
    times = []

    for n in range(n_min, n_max + 1):
        print(f"正在测试 N={n}...")
        start = time.time()
        solve_n_queens(n, show_all=False)
        end = time.time()
        duration = end - start
        ns.append(n)
        times.append(duration)

    # 绘制时间增长曲线
    plt.plot(ns, times, marker='o')
    plt.title("N皇后问题运行时间")
    plt.xlabel("N")
    plt.ylabel("时间（秒）")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("runtime_plot.png")
    plt.show()

    print("✅ 运行时间曲线已生成并保存为 runtime_plot.png")

def is_valid(row, col, cols, diag1, diag2):
    return col not in cols and (row - col) not in diag1 and (row + col) not in diag2

def print_board(queens, n):
    board = []
    for i in range(n):
        row = ['.'] * n
        row[queens[i]] = 'Q'
        board.append(''.join(row))
    print('\n'.join(board))
    print('-' * n)

def solve_n_queens(n, show_all=True):
    solutions = []
    queens = [-1] * n
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row):
        if row == n:
            solutions.append(queens[:])
            if show_all:
                print_board(queens, n)
            return

        for col in range(n):
            if not is_valid(row, col, cols, diag1, diag2):
                continue
            queens[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    start_time = time.time()
    backtrack(0)
    end_time = time.time()

    print(f"\n✅ 解的总数: {len(solutions)}")
    print(f"⏱️ 运行时间: {end_time - start_time:.4f} 秒")
    return solutions

def main():
    while True:
        try:
            n = int(input("请输入皇后个数 N (N ≥ 4)："))
            if n >= 4:
                break
            print("❗ N 必须大于等于 4。")
        except ValueError:
            print("❗ 请输入一个整数。")

    choice = input("是否输出所有解？(y/n): ").strip().lower()
    show_all = (choice == 'y')

    solve_n_queens(n, show_all)

if __name__ == "__main__":
    main()
    auto_test = input("是否进行N=4到12的运行时间测试？(y/n): ").strip().lower()
    if auto_test == 'y':
        test_runtime()