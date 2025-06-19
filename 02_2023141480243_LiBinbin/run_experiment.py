import random
import matplotlib.pyplot as plt
from prisoners_simulation import random_search_strategy, cyclic_search_strategy  # 确保文件名正确

def run_experiment(N, K, T):
    random_success_counts = []
    cyclic_success_counts = []

    for _ in range(T):
        random_success = random_search_strategy(N, K)
        cyclic_success = cyclic_search_strategy(N, K)

        random_success_counts.append(random_success)
        cyclic_success_counts.append(cyclic_success)

    return random_success_counts, cyclic_success_counts

def plot_results(random_counts, cyclic_counts):
    plt.figure(figsize=(12, 6))

    # 绘制随机搜索成功人数的分布
    plt.subplot(1, 2, 1)
    plt.hist(random_counts, bins=range(0, max(random_counts) + 1), alpha=0.7, color='blue', edgecolor='black')
    plt.title('Random Search Success Distribution')
    plt.xlabel('Number of Successful Prisoners')
    plt.ylabel('Frequency')

    # 绘制循环策略成功人数的分布
    plt.subplot(1, 2, 2)
    plt.hist(cyclic_counts, bins=range(0, max(cyclic_counts) + 1), alpha=0.7, color='green', edgecolor='black')
    plt.title('Cyclic Search Success Distribution')
    plt.xlabel('Number of Successful Prisoners')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 设置实验参数
    N = 100  # 囚犯数量
    K = 50   # 每人尝试次数
    T = 10000  # 模拟轮次

    random_counts, cyclic_counts = run_experiment(N, K, T)
    plot_results(random_counts, cyclic_counts)