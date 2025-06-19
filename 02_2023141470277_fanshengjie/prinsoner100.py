import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm

# 设置Matplotlib使用非交互式后端以避免错误
matplotlib.use('Agg')  # 使用Agg后端，不显示图形但可以保存
plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def simulate_prisoners(N=100, K=50, T=10000):
    """
    模拟囚犯问题的两种策略
    :param N: 囚犯数量
    :param K: 每人尝试次数
    :param T: 模拟轮次
    :return: 随机策略成功率, 循环策略成功率, 循环策略每轮成功人数
    """
    # 结果存储
    random_success = np.zeros(T, dtype=bool)
    cycle_success = np.zeros(T, dtype=bool)
    cycle_success_counts = np.zeros(T, dtype=int)

    # 随机策略模拟
    print(f"模拟随机策略 (N={N}, K={K})...")
    for i in tqdm(range(T), desc="随机策略进度"):
        # 生成随机排列
        boxes = np.random.permutation(N)
        found = np.zeros(N, dtype=bool)

        # 为每个囚犯生成随机选择的盒子索引
        choices = np.array([np.random.choice(N, K, replace=False) for _ in range(N)])

        # 检查每个囚犯是否找到自己的编号
        for prisoner in range(N):
            selected_boxes = boxes[choices[prisoner]]
            if prisoner in selected_boxes:
                found[prisoner] = True
            else:
                # 如果有一个失败，整个实验失败
                break

        random_success[i] = np.all(found)

    # 循环策略模拟（使用循环分解优化）
    print(f"模拟循环策略 (N={N}, K={K})...")
    for i in tqdm(range(T), desc="循环策略进度"):
        # 生成随机排列
        boxes = np.random.permutation(N)
        visited = np.zeros(N, dtype=bool)
        total_failures = 0

        # 循环分解
        for start in range(N):
            if not visited[start]:
                cycle_length = 0
                current = start
                while not visited[current]:
                    visited[current] = True
                    cycle_length += 1
                    current = boxes[current]

                # 记录失败囚犯数
                if cycle_length > K:
                    total_failures += cycle_length

        cycle_success_counts[i] = N - total_failures
        cycle_success[i] = (total_failures == 0)

    return random_success, cycle_success, cycle_success_counts


def analyze_results(random_success, cycle_success, cycle_success_counts, N, K):
    """分析并可视化结果"""
    # 计算成功率
    random_rate = np.mean(random_success)
    cycle_rate = np.mean(cycle_success)
    avg_success_count = np.mean(cycle_success_counts)
    std_success_count = np.std(cycle_success_counts)

    print(f"\n参数: N={N}, K={K}")
    print(f"随机策略成功率: {random_rate:.6f} ({np.sum(random_success)}/{len(random_success)})")
    print(f"循环策略成功率: {cycle_rate:.6f} ({np.sum(cycle_success)}/{len(cycle_success)})")
    print(f"循环策略平均成功人数: {avg_success_count:.2f}±{std_success_count:.2f}/{N}")

    # 循环策略成功人数分布
    plt.figure(figsize=(10, 6))
    plt.hist(cycle_success_counts, bins=np.arange(-0.5, N + 1.5, 1),
             density=True, alpha=0.7, color='skyblue')
    plt.axvline(x=N, color='r', linestyle='--', label='全体成功')
    plt.axvline(x=N / 2, color='g', linestyle='--', label='50%成功')
    plt.title(f'循环策略成功人数分布 (N={N}, K={K}, 模拟轮次={len(cycle_success_counts)})')
    plt.xlabel('成功囚犯人数')
    plt.ylabel('概率密度')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'cycle_success_N{N}_K{K}.png')
    plt.close()  # 关闭图形以释放内存

    # 成功率随轮次变化
    plt.figure(figsize=(10, 6))
    plt.plot(np.cumsum(random_success) / (np.arange(len(random_success)) + 1),
             label=f'随机策略 (最终={random_rate:.4f})', color='blue')
    plt.plot(np.cumsum(cycle_success) / (np.arange(len(cycle_success)) + 1),
             label=f'循环策略 (最终={cycle_rate:.4f})', color='red')
    plt.axhline(y=cycle_rate, color='orange', linestyle='--', alpha=0.5)
    plt.title(f'成功率随模拟轮次变化 (N={N}, K={K})')
    plt.xlabel('模拟轮次')
    plt.ylabel('累计成功率')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'success_rate_N{N}_K{K}.png')
    plt.close()  # 关闭图形以释放内存

    return random_rate, cycle_rate


if __name__ == "__main__":
    # 设置模拟轮次
    T = 5000  # 减少模拟轮次以加快多组参数运行速度

    # 定义多组参数 (N, K)
    param_sets = [
        (50, 25),  # 标准比例：K/N = 0.5
        (100, 50),  # 标准比例：K/N = 0.5
        (200, 100),  # 标准比例：K/N = 0.5
        (50, 10),  # K/N = 0.2
        (50, 40),  # K/N = 0.8
        (100, 30),  # K/N = 0.3
        (100, 70),  # K/N = 0.7
    ]

    # 存储结果
    results = []

    for i, (N, K) in enumerate(param_sets):
        print(f"\n{'=' * 50}")
        print(f"开始模拟组 {i + 1}/{len(param_sets)}: N={N}, K={K}, T={T}")

        # 运行模拟
        random_success, cycle_success, cycle_counts = simulate_prisoners(N, K, T)

        # 分析结果
        random_rate, cycle_rate = analyze_results(
            random_success, cycle_success, cycle_counts, N, K
        )

        # 记录结果
        results.append((N, K, random_rate, cycle_rate))

    # 输出所有参数组的成功率对比
    print("\n\n" + "=" * 50)
    print("不同参数下的成功率对比:")
    print("N\tK\tK/N\t随机策略成功率\t循环策略成功率")
    for N, K, random_rate, cycle_rate in results:
        print(f"{N}\t{K}\t{K / N:.2f}\t{random_rate:.6f}\t\t{cycle_rate:.6f}")

    # 可视化成功率随K/N比例的变化
    plt.figure(figsize=(10, 6))
    ratios = [K / N for N, K, _, _ in results]
    random_rates = [r for _, _, r, _ in results]
    cycle_rates = [r for _, _, _, r in results]

    # 按K/N排序
    sorted_indices = np.argsort(ratios)
    ratios = [ratios[i] for i in sorted_indices]
    random_rates = [random_rates[i] for i in sorted_indices]
    cycle_rates = [cycle_rates[i] for i in sorted_indices]

    plt.plot(ratios, random_rates, 'bo-', label='随机策略')
    plt.plot(ratios, cycle_rates, 'ro-', label='循环策略')

    plt.title('不同K/N比例下的策略成功率对比')
    plt.xlabel('K/N比例')
    plt.ylabel('成功率')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('strategy_comparison.png')
    plt.close()

    print("\n模拟完成！所有图表已保存为PNG文件")