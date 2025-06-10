import numpy as np
import matplotlib.pyplot as plt


plt.rc("font", family='STXingkai')#family是设置的字体
def simulate_prisoners(N=100, K=50, T=10000, strategy='loop'):
    success_count = 0

    for _ in range(T):
        # 随机排列盒子中的编号
        boxes = np.random.permutation(N) + 1  # 编号1-N

        all_success = True

        for prisoner in range(1, N + 1):
            found = False
            opened = 0
            current_box = prisoner

            if strategy == 'random':
                # 随机策略：随机选择K个盒子
                boxes_to_open = np.random.choice(N, K, replace=False) + 1
                for box in boxes_to_open:
                    opened += 1
                    if boxes[box - 1] == prisoner:
                        found = True
                        break
            elif strategy == 'loop':
                # 循环策略：从自己的编号开始追踪
                current_box = prisoner
                for _ in range(K):
                    opened += 1
                    if boxes[current_box - 1] == prisoner:
                        found = True
                        break
                    current_box = boxes[current_box - 1]

            if not found:
                all_success = False
                break

        if all_success:
            success_count += 1

    success_rate = success_count / T
    return success_rate


def compare_strategies(N=100, K=50, T=10000):
    print(f"模拟参数: N={N}, K={K}, T={T}")

    print("\n运行随机策略...")
    random_rate = simulate_prisoners(N, K, T, 'random')
    print(f"随机策略成功率: {random_rate:.4f}")

    print("\n运行循环策略...")
    loop_rate = simulate_prisoners(N, K, T, 'loop')
    print(f"循环策略成功率: {loop_rate:.4f}")

    return random_rate, loop_rate


def plot_success_distribution(N=100, K=50, T=1000):
    successes = []

    for _ in range(T):
        boxes = np.random.permutation(N) + 1
        all_success = True

        for prisoner in range(1, N + 1):
            found = False
            current_box = prisoner
            for _ in range(K):
                if boxes[current_box - 1] == prisoner:
                    found = True
                    break
                current_box = boxes[current_box - 1]

            if not found:
                all_success = False
                break

        successes.append(1 if all_success else 0)

    # 计算移动平均以平滑曲线
    window_size = 50
    moving_avg = np.convolve(successes, np.ones(window_size) / window_size, mode='valid')

    plt.figure(figsize=(12, 6))
    plt.plot(range(len(moving_avg)), moving_avg)
    plt.xlabel('试验批次 (每50次移动平均)')
    plt.ylabel('成功率')
    plt.title(f'循环策略成功率的分布 (N={N}, K={K})')
    plt.axhline(y=np.mean(successes), color='r', linestyle='--', label=f'平均成功率: {np.mean(successes):.4f}')
    plt.legend()
    plt.grid()
    plt.show()


def analyze_parameters():
    parameters = [
        (100, 50),
        (50, 25),
        (30, 15),
        (20, 10),
        (10, 5)
    ]

    results = []

    for N, K in parameters:
        print(f"\n分析 N={N}, K={K}...")
        random_rate, loop_rate = compare_strategies(N, K, T=5000)
        results.append((N, K, random_rate, loop_rate))

    # 显示结果表格
    print("\n结果汇总:")
    print("N\tK\t随机策略\t循环策略")
    for N, K, random_rate, loop_rate in results:
        print(f"{N}\t{K}\t{random_rate:.4f}\t\t{loop_rate:.4f}")

    # 绘制成功率对比
    plt.figure(figsize=(10, 6))
    x = range(len(results))
    plt.plot(x, [r[2] for r in results], 'o-', label='随机策略')
    plt.plot(x, [r[3] for r in results], 's-', label='循环策略')
    plt.xticks(x, [f'N={r[0]}\nK={r[1]}' for r in results])
    plt.xlabel('参数 (N, K)')
    plt.ylabel('成功率')
    plt.title('不同参数下的策略成功率对比')
    plt.legend()
    plt.grid()
    plt.show()


# 主程序
if __name__ == "__main__":
    # 基本参数对比
    random_rate, loop_rate = compare_strategies(T=10000)

    # 循环策略的成功率分布
    plot_success_distribution(T=5000)

    # 不同参数分析
    analyze_parameters()