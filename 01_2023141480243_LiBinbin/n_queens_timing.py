import time
import matplotlib.pyplot as plt
from n_queens import solve_n_queens  # 假设 n_queens.py 和 n_queens_timing.py 在同一目录下

def time_test():
    ns = list(range(4, 13))
    durations = []

    for n in ns:
        start_time = time.time()
        solve_n_queens(n)
        duration = time.time() - start_time
        durations.append(duration)
        print(f"N={n}, Time taken: {duration:.6f} seconds")

    # 绘制时间增长曲线
    plt.figure(figsize=(10, 5))
    plt.plot(ns, durations, marker='o')
    plt.title('N-Queens Problem Time Complexity')
    plt.xlabel('N (Size of the board)')
    plt.ylabel('Time taken (seconds)')
    plt.xticks(ns)
    plt.grid(True)

    # 添加数值标注
    for i, duration in enumerate(durations):
        plt.text(ns[i], duration, f"{duration:.6f}", ha='center', va='bottom')

    plt.savefig('n_queens_timing.png')  # 保存为图片
    plt.show()

if __name__ == "__main__":
    time_test()