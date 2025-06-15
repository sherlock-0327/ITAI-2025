import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm


def generate_permutation(N):
    """生成一个随机的排列，0到N-1"""
    return np.random.permutation(N)


def simulate_random_strategy(perm, K):
    """
    模拟随机策略
    :param perm: 排列，表示盒子中的纸条
    :param K: 每个囚犯最大尝试次数
    :return: 成功找到编号的囚犯人数
    """
    N = len(perm)
    success_count = 0
    # 对每个囚犯进行模拟
    for prisoner in range(N):
        # 随机选择K个盒子（无放回抽样）
        boxes_to_open = np.random.choice(N, size=K, replace=False)
        # 检查这些盒子中是否有囚犯的编号
        if prisoner in perm[boxes_to_open]:
            success_count += 1
    return success_count


def simulate_cycle_strategy(perm, K):
    """
    模拟循环策略
    :param perm: 排列，表示盒子中的纸条
    :param K: 每个囚犯最大尝试次数
    :return: 成功找到编号的囚犯人数
    """
    N = len(perm)
    visited = np.zeros(N, dtype=bool)
    success_count = 0

    for i in range(N):
        if not visited[i]:
            # 开始一个新的循环
            cycle = [i]
            visited[i] = True
            current = perm[i]
            # 跟踪循环直到回到起点
            while current != i:
                cycle.append(current)
                visited[current] = True
                current = perm[current]
            cycle_length = len(cycle)
            # 如果循环长度小于等于K，所有囚犯都能找到编号
            if cycle_length <= K:
                success_count += cycle_length
    return success_count


def run_simulation(N=100, K=50, T=10000):
    """
    运行模拟实验
    :param N: 囚犯数量
    :param K: 每人尝试次数
    :param T: 模拟轮次
    :return: 随机策略结果，循环策略结果
    """
    random_success_counts = []
    cycle_success_counts = []
    random_global_success = 0
    cycle_global_success = 0

    for _ in tqdm(range(T), desc="Running simulations"):
        perm = generate_permutation(N)

        # 运行随机策略
        random_count = simulate_random_strategy(perm, K)
        random_success_counts.append(random_count)
        if random_count == N:
            random_global_success += 1

        # 运行循环策略
        cycle_count = simulate_cycle_strategy(perm, K)
        cycle_success_counts.append(cycle_count)
        if cycle_count == N:
            cycle_global_success += 1

    # 计算整体成功率
    random_success_rate = random_global_success / T
    cycle_success_rate = cycle_global_success / T

    return {
        'random_success_rate': random_success_rate,
        'cycle_success_rate': cycle_success_rate,
        'random_success_counts': random_success_counts,
        'cycle_success_counts': cycle_success_counts
    }


def plot_results(results, N, K, T):
    """绘制结果"""
    # 成功率对比
    plt.figure(figsize=(10, 6))
    plt.bar(['Random Strategy', 'Cycle Strategy'],
            [results['random_success_rate'], results['cycle_success_rate']],
            color=['skyblue', 'lightgreen'])
    plt.ylabel('Success Rate')
    plt.title(f'Success Rate Comparison (N={N}, K={K}, T={T})')
    plt.ylim(0, 0.35)
    plt.grid(axis='y')
    plt.show()

    # 循环策略下成功人数分布
    plt.figure(figsize=(10, 6))
    sns.histplot(results['cycle_success_counts'], bins=20, kde=True)
    plt.axvline(x=N, color='r', linestyle='--', label='All Success')
    plt.xlabel('Number of Successful Prisoners')
    plt.ylabel('Frequency')
    plt.title(f'Cycle Strategy: Distribution of Successful Prisoners (N={N}, K={K}, T={T})')
    plt.legend()
    plt.grid(True)
    plt.show()


def parameter_analysis(T=10000):
    """参数分析：不同N和K下的成功率变化"""
    params = [
        (100, 50),
        (50, 25),
        (100, 30),
        (100, 70),
        (200, 100)
    ]

    results = []
    for N, K in params:
        print(f"Running for N={N}, K={K}")
        res = run_simulation(N, K, T)
        results.append((N, K, res['cycle_success_rate']))

    # 打印结果
    print("\nParameter Analysis Results:")
    for N, K, rate in results:
        print(f"N={N}, K={K}: Success Rate = {rate:.4f}")


if __name__ == "__main__":
    # 默认参数模拟
    N, K, T = 100, 50, 10000
    results = run_simulation(N, K, T)

    # 打印结果
    print(f"Random Strategy Success Rate: {results['random_success_rate']:.6f}")
    print(f"Cycle Strategy Success Rate: {results['cycle_success_rate']:.6f}")

    # 绘图
    plot_results(results, N, K, T)

    # 参数分析
    parameter_analysis(T=5000)