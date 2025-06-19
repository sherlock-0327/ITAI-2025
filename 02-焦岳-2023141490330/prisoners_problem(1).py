
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def run_cycle_strategy(n=100, k=50, t=10000):
    success = 0
    max_cycles = []

    for _ in tqdm(range(t), desc="模拟中"):
        boxes = np.random.permutation(n) + 1
        visited = [False] * n
        max_len = 0

        for i in range(n):
            if not visited[i]:
                cnt, j = 0, i
                while not visited[j]:
                    visited[j] = True
                    j = boxes[j] - 1
                    cnt += 1
                max_len = max(max_len, cnt)

        max_cycles.append(max_len)
        if max_len <= k:
            success += 1

    return success / t, max_cycles

def plot_results(success_rate, max_cycles, k):
    print(f"成功率: {success_rate:.2%}")
    plt.hist(max_cycles, bins=np.arange(1, 102) - 0.5, density=True, alpha=0.7)
    plt.axvline(k, color='r', linestyle='--', label=f"K = {k}")
    plt.title("最大环长度分布")
    plt.xlabel("最大环长度")
    plt.ylabel("概率密度")
    plt.grid(True, linestyle=':')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    rate, cycles = run_cycle_strategy()
    plot_results(rate, cycles, 50)
