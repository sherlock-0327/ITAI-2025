import time
import matplotlib.pyplot as plt
import matplotlib

# 设置字体以避免中文乱码警告
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 判断是否可以放置皇后
def is_safe(queens, row, col):
    for r, c in enumerate(queens):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

# 回溯法求解基本实现
def backtrack_basic(n, row, queens, solutions, find_one=False):
    if row == n:
        solutions.append(queens[:])
        return find_one
    for col in range(n): # 遍历当前行的所有列
        if is_safe(queens, row, col): # 判断是否冲突
            queens.append(col)
            if backtrack_basic(n, row + 1, queens, solutions, find_one):
                return True
            queens.pop() # 回溯
    return False

def solve_n_queens_basic(n, find_one=False):
    solutions = []
    backtrack_basic(n, 0, [], solutions, find_one)
    return solutions

# 对称性优化
def backtrack_symmetry(n, row, queens, solutions):
    if row == n:
        solutions.append(queens[:])
        return
    cols = range(n // 2) if row == 0 else range(n)  # 剪枝关键点
    for col in cols:
        if is_safe(queens, row, col):
            queens.append(col)
            backtrack_symmetry(n, row + 1, queens, solutions)
            queens.pop()

def solve_n_queens_symmetry(n):
    solutions = []
    backtrack_symmetry(n, 0, [], solutions)
    mirrored = []
    if n % 2 == 1: # 奇数补偿
        col = n // 2
        queens = [col] # 将第 0 行的皇后放在中间列；
        backtrack_symmetry(n, 1, queens, mirrored)
    total = solutions + [ [n - 1 - c if r == 0 else c for r, c in enumerate(sol)] for sol in solutions ] + mirrored # 镜像生成
    return total


# 位运算优化方法（支持 n <= 32）
def solve_n_queens_bitwise(n):
    results = []

    def dfs(row, cols, pies, nas, state):
        if row == n:
            results.append(state[:])
            return
        bits = (~(cols | pies | nas)) & ((1 << n) - 1) # 计算可选位置
        while bits:
            p = bits & -bits  # 取最低位的1
            col = bin(p - 1).count("1")
            state.append(col)
            dfs(row + 1, cols | p, (pies | p) << 1, (nas | p) >> 1, state)
            state.pop()
            bits &= bits - 1 # 去除已尝试的位置，继续尝试其他可能

    dfs(0, 0, 0, 0, [])
    return results


# 打印解
def print_solutions(solutions, n):
    for idx, sol in enumerate(solutions):
        print(f"\n第 {idx + 1} 个解：")
        for row in sol:
            print("".join("Q" if c == row else "." for c in range(n)))


# 主程序：交互模式
def main():
    print("=== N 皇后问题求解器 ===")
    while True:
        try:
            N = int(input("请输入皇后数量 N（N >= 4）："))
            if N >= 4:
                break
            print("输入必须大于等于 4")
        except ValueError:
            print("请输入有效整数")

    while True:
        mode = input("输出模式：输入 'a' 输出所有解，输入 '1' 仅输出一个解：").strip().lower()
        if mode in ['a', '1']:
            break
        print("输入无效，请重新输入 'a' 或 '1'")
    only_one = mode == '1'

    start_time = time.time()
    solutions = solve_n_queens_basic(N, find_one=only_one)
    end_time = time.time()

    print_solutions(solutions, N)
    print(f"\n解的总数: {len(solutions)}")
    print(f"耗时: {end_time - start_time:.4f} 秒")


# 通用实验函数
def run_experiment(solver_func, label):
    Ns = list(range(4, 13))
    times = []
    counts = []

    for n in Ns:
        start = time.time()
        sol = solver_func(n)
        end = time.time()
        times.append(end - start)
        counts.append(len(sol))
        print(f"{label} | N={n}: 解数={len(sol)}, 时间={end-start:.4f}s")

    return Ns, times, counts


def plot_all_results(Ns, times_list, labels, counts):
    plt.figure(figsize=(12, 8))

    # 子图 1：基本回溯法 时间图
    plt.subplot(2, 2, 1)
    plt.plot(Ns, times_list[0], marker='o')
    plt.title(f"{labels[0]} - 时间增长")
    plt.xlabel("N")
    plt.ylabel("运行时间 (秒)")
    plt.grid(True)

    # 子图 2：对称剪枝法 时间图
    plt.subplot(2, 2, 2)
    plt.plot(Ns, times_list[1], marker='o')
    plt.title(f"{labels[1]} - 时间增长")
    plt.xlabel("N")
    plt.ylabel("运行时间 (秒)")
    plt.grid(True)

    # 子图 3：位运算优化法 时间图
    plt.subplot(2, 2, 3)
    plt.plot(Ns, times_list[2], marker='o')
    plt.title(f"{labels[2]} - 时间增长")
    plt.xlabel("N")
    plt.ylabel("运行时间 (秒)")
    plt.grid(True)

    # 子图 4：所有方法的解数增长图
    plt.subplot(2, 2, 4)
    plt.plot(Ns, counts, marker='o', color='green')
    plt.title("所有方法 - 解数增长趋势")
    plt.xlabel("N")
    plt.ylabel("解的总数")
    plt.grid(True)

    plt.tight_layout()
    plt.show()



# 示例运行
if __name__ == "__main__":
    # 交互模式
    main()

    # 方法对比
    Ns1, t1, c1 = run_experiment(solve_n_queens_basic, "基本回溯法")
    Ns2, t2, c2 = run_experiment(solve_n_queens_symmetry, "对称剪枝法")
    Ns3, t3, c3 = run_experiment(solve_n_queens_bitwise, "位运算优化法")

    # 四图合一展示
    plot_all_results(Ns1, [t1, t2, t3], ["基本回溯法", "对称剪枝法", "位运算优化法"], c1)
