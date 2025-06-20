import numpy as np
import matplotlib.pyplot as plt
import time

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_params():
    """获取用户输入。如果用户直接回车，则使用默认值。"""
    defaults = {'N': 100, 'K': 50, 'T': 10000}

    print("--- 参数设置 ---")
    print("将在下方提示您输入 N, K, T 的值。直接按回车可使用默认值。")

    while True:
        try:
            n_str = input(f"请输入囚犯数量 N (默认: {defaults['N']}): ")
            N = int(n_str) if n_str else defaults['N']

            k_str = input(f"请输入尝试次数 K (默认: {defaults['K']}): ")
            K = int(k_str) if k_str else defaults['K']

            t_str = input(f"请输入模拟轮次 T (默认: {defaults['T']}): ")
            T = int(t_str) if t_str else defaults['T']

            if N > 0 and 0 < K <= N and T > 0:
                return N, K, T
            else:
                print("错误: 参数不合法 (要求 N>0, 0<K<=N, T>0)，请重新输入。")
        except ValueError:
            print("错误: 输入无效，请输入一个整数或直接回车。")


def find_max_cycle_length(boxes: np.ndarray) -> int:
    """高效计算排列中的最大循环长度 (O(N) 复杂度)。"""
    N = len(boxes)
    visited = np.zeros(N, dtype=bool)
    max_len = 0
    for i in range(N):
        if not visited[i]:
            current_len = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = boxes[j]
                current_len += 1
            if current_len > max_len:
                max_len = current_len
    return max_len


def run_simulation(N: int, K: int, T: int, use_cycle_strategy: bool):
    """运行模拟并返回结果。"""
    if not use_cycle_strategy:  # 随机策略
        success_count = 0
        for _ in range(T):
            boxes = np.random.permutation(N)
            # 模拟一个囚犯
            prisoner_success = False
            for prisoner_id in range(N):
                chosen_boxes = np.random.choice(N, K, replace=False)
                if prisoner_id in boxes[chosen_boxes]:
                    prisoner_success = True
                else:  # 任何一个囚犯失败，则本轮失败
                    prisoner_success = False
                    break
            if prisoner_success:
                success_count += 1
        return success_count / T, None, None

    # 循环策略 (优化版)
    max_cycle_lengths = np.zeros(T, dtype=int)
    for i in range(T):
        boxes = np.random.permutation(N)
        max_cycle_lengths[i] = find_max_cycle_length(boxes)

    success_outcomes = (max_cycle_lengths <= K)
    success_rate = success_outcomes.mean()

    return success_rate, max_cycle_lengths, success_outcomes


def calculate_theoretical_rate(N: int, K: int) -> float:
    """计算循环策略的理论成功率。"""
    if K >= N: return 1.0
    return 1.0 - sum(1.0 / i for i in range(K + 1, N + 1))


def plot_results(max_lengths: np.ndarray, outcomes: np.ndarray, N: int, K: int, T: int, rate: float,
                 theory_rate: float):
    """统一绘制所有结果图形。"""
    # 图1: 最长循环长度分布直方图
    plt.figure(figsize=(10, 6))
    plt.hist(max_lengths, bins=range(1, N + 2), alpha=0.8, color='skyblue', density=True)
    plt.axvline(K, color='r', linestyle='--', linewidth=2, label=f'成功临界线 K={K}')
    plt.title(f'策略2: 最长循环长度分布 (N={N}, T={T})', fontsize=15)
    plt.xlabel('最长循环长度')
    plt.ylabel('频率(概率密度)')
    plt.legend()
    plt.grid(axis='y', alpha=0.5)
    plt.text(0.95, 0.95, f'模拟成功率: {rate:.4f}', ha='right', va='top', transform=plt.gca().transAxes,
             bbox=dict(fc='wheat', alpha=0.5))
    plt.show()

    # 图2: 累计成功次数图
    plt.figure(figsize=(10, 6))
    cumulative_successes = np.cumsum(outcomes)
    trials = np.arange(1, T + 1)
    plt.plot(trials, cumulative_successes, label='实际累计成功次数', color='green')
    plt.plot(trials, trials * theory_rate, label='理论期望成功次数', color='red', linestyle='--')
    plt.title(f'策略2: 累计成功天数分布 (T={T})', fontsize=15)
    plt.xlabel('模拟轮次(天)')
    plt.ylabel('累计成功次数')
    plt.legend()
    plt.grid(alpha=0.5)
    plt.xlim(1, T)
    plt.show()


def main():
    """主函数，执行所有模拟和分析"""
    N, K, T = get_params()

    print(f"\n已采用参数: N={N}, K={K}, T={T}")
    print("\n" + "=" * 40)

    # --- 策略1: 随机搜索 ---
    print("\n>>> 正在执行策略1: 随机搜索...")
    start_time = time.time()
    random_rate, _, _ = run_simulation(N, K, T, use_cycle_strategy=False)
    print(f"  - 模拟成功率: {random_rate:.8f} (理论上几乎为0)")
    print(f"  - 执行耗时: {time.time() - start_time:.4f} 秒")

    # --- 策略2: 循环策略 ---
    print("\n>>> 正在执行策略2: 循环跟随 (已优化)...")
    start_time = time.time()
    cycle_rate, max_lengths, outcomes = run_simulation(N, K, T, use_cycle_strategy=True)
    theory_rate = calculate_theoretical_rate(N, K)
    print(f"  - 模拟成功率: {cycle_rate:.4f}")
    print(f"  - 理论成功率: {theory_rate:.4f}")
    print(f"  - 执行耗时: {time.time() - start_time:.4f} 秒")

    # --- 图形化分析 ---
    if max_lengths is not None:
        print("\n>>> 生成策略2的分析图形...")
        plot_results(max_lengths, outcomes, N, K, T, cycle_rate, theory_rate)

    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()