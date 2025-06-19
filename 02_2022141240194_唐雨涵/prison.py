import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib


# 设置字体以避免中文乱码警告
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False


# 盒子生成：随机生成一个长度为 N 的排列，模拟盒子中纸条编号
def generate_boxes(N):
    return np.random.permutation(N)

# 随机策略：囚犯随机打开 K 个盒子寻找自己的编号
def simulate_random_strategy(N, K):
    boxes = generate_boxes(N)
    for prisoner in range(N):
        choices = np.random.choice(N, K, replace=False)
        if prisoner not in boxes[choices]:
            return False
    return True

# 循环策略：从与囚犯编号相同的盒子出发进行最多 K 次跳转
def simulate_loop_strategy(N, K):
    boxes = generate_boxes(N)
    for prisoner in range(N):
        current = prisoner
        for _ in range(K):
            if boxes[current] == prisoner:
                break
            current = boxes[current]
        else:
            return False
    return True


# 单次模拟（ N: 囚犯数，K: 尝试次数，T: 总仿真次数）
def run_simulation(strategy_func, N=100, K=50, T=10000):
    success_count = 0
    results = []
    for _ in tqdm(range(T), desc=f"Simulating {strategy_func.__name__}"):
        success = strategy_func(N, K)
        results.append(success)
        if success:
            success_count += 1
    success_rate = success_count / T
    return success_rate, results



# 单次模拟结果：成功/失败对比图
def plot_results(results_random, results_loop):
    labels = ['失败', '成功']
    random_counts = [results_random.count(False), results_random.count(True)]
    loop_counts = [results_loop.count(False), results_loop.count(True)]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width / 2, random_counts, width, label='随机策略')
    ax.bar(x + width / 2, loop_counts, width, label='循环策略')

    ax.set_ylabel('次数')
    ax.set_title('100囚犯问题策略对比')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


# 多次模拟实验
def repeat_simulations(strategy_func, N=100, K=50, T=10000, repeat=10):
    success_rates = []

    for i in range(repeat):
        print(f"\n第 {i + 1} 次模拟：")
        success_rate, _ = run_simulation(strategy_func, N, K, T)
        success_rates.append(success_rate)
        print(f"{strategy_func.__name__} 第 {i + 1} 次成功率：{success_rate:.4f}")

    avg_rate = np.mean(success_rates)
    print(f"\n{strategy_func.__name__} 平均成功率：{avg_rate:.4f}")
    return success_rates


# 多轮模拟成功率折线图
def plot_multiple_success_rates(rates_random, rates_loop):

    rounds = np.arange(1, len(rates_random) + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(rounds, rates_random, marker='o', label='随机策略')
    plt.plot(rounds, rates_loop, marker='s', label='循环策略')

    plt.xlabel('模拟轮次')
    plt.ylabel('成功率')
    plt.title('多轮模拟中两种策略的成功率变化')
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()


#主程序
if __name__ == "__main__":
    N = 100  # 囚犯数量
    K = 50   # 每人最多尝试次数
    T = 10000  # 每轮仿真次数
    repeat = 10  # 多轮模拟次数

    print("请选择模拟模式：")
    print("1 - 单次模拟，绘制成功/失败对比图")
    print("2 - 多次模拟，绘制成功率折线图")

    mode = input("请输入选项（1 或 2）：").strip()

    if mode == "1":
        print("开始单次模拟...")
        rate_random, results_random = run_simulation(simulate_random_strategy, N, K, T)
        rate_loop, results_loop = run_simulation(simulate_loop_strategy, N, K, T)

        print(f"\n随机策略成功率：{rate_random:.4f}")
        print(f"循环策略成功率：{rate_loop:.4f}")


        plot_results(results_random, results_loop)

    elif mode == "2":
        print("开始随机策略多轮模拟：")
        rates_random = repeat_simulations(simulate_random_strategy, N, K, T, repeat)

        print("\n开始循环策略多轮模拟：")
        rates_loop = repeat_simulations(simulate_loop_strategy, N, K, T, repeat)

        plot_multiple_success_rates(rates_random, rates_loop)

    else:
        print("无效输入，请输入 1 或 2。")