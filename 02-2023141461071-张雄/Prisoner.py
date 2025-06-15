import numpy as np
import matplotlib.pyplot as plt
import time

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 支持中文显示
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


class PrisonerSimulator:
    def __init__(self, n=100, max_attempts=50):
        """初始化囚徒问题模拟器"""
        self.n = n  # 囚徒数量
        self.k = max_attempts  # 每个囚徒最多尝试次数

    def generate_boxes(self):
        """生成随机的盒子排列（0-99的随机排列）"""
        return np.random.permutation(self.n)

    def random_strategy(self, boxes, pid):
        """随机搜索策略：随机选择k个盒子"""
        # 随机选择不重复的盒子
        chosen = np.random.choice(self.n, size=min(self.k, self.n), replace=False)
        for box in chosen:
            if boxes[box] == pid:  # 找到自己的编号
                return True
        return False

    def cycle_strategy(self, boxes, pid):
        """循环策略：从自己编号的盒子开始，按纸条内容跳转"""
        current = pid  # 当前打开的盒子编号
        attempts = 0
        while attempts < self.k:
            paper = boxes[current]  # 盒子里的纸条编号
            attempts += 1
            if paper == pid:  # 找到自己的编号
                return True
            current = paper  # 跳转到下一个盒子
        return False

    def simulate_round(self, strategy='random'):
        """模拟单轮实验，返回是否全体成功和成功人数"""
        boxes = self.generate_boxes()
        success_count = 0
        for pid in range(self.n):
            if strategy == 'random':
                success = self.random_strategy(boxes, pid)
            elif strategy == 'cycle':
                success = self.cycle_strategy(boxes, pid)
            else:
                raise ValueError("策略必须为'random'或'cycle'")
            if success:
                success_count += 1
        all_success = (success_count == self.n)
        return all_success, success_count

    def run_simulation(self, n_sims=10000, strategy='random', verbose=True):
        """运行多轮仿真，返回统计结果"""
        all_success_cnt = 0
        success_list = []
        if verbose:
            print(f"运行{strategy}策略仿真...")
        for i in range(n_sims):
            if verbose and (i + 1) % 1000 == 0:
                print(f"进度: {i + 1}/{n_sims}")
            all_success, success_cnt = self.simulate_round(strategy)
            if all_success:
                all_success_cnt += 1
            success_list.append(success_cnt)
        success_rate = all_success_cnt / n_sims
        return {
            'strategy': strategy,
            'n_sims': n_sims,
            'all_success': all_success_cnt,
            'success_rate': success_rate,
            'success_list': success_list,
            'avg_success': np.mean(success_list),
            'std_success': np.std(success_list)
        }

    def compare_strategies(self, n_sims=10000):
        """比较两种策略的性能"""
        print(f"开始仿真比较 - 囚徒数: {self.n}, 最大尝试: {self.k}")
        print(f"仿真轮次: {n_sims}")
        print("=" * 60)

        # 运行随机策略
        start = time.time()
        res_random = self.run_simulation(n_sims, 'random')
        time_random = time.time() - start

        # 运行循环策略
        start = time.time()
        res_cycle = self.run_simulation(n_sims, 'cycle')
        time_cycle = time.time() - start

        # 打印结果
        print(f"\n随机策略结果:")
        print(f"  全体成功次数: {res_random['all_success']}")
        print(f"  全体成功率: {res_random['success_rate']:.6f} ({res_random['success_rate'] * 100:.4f}%)")
        print(f"  平均成功人数: {res_random['avg_success']:.2f} ± {res_random['std_success']:.2f}")
        print(f"  运行时间: {time_random:.2f}秒")

        print(f"\n循环策略结果:")
        print(f"  全体成功次数: {res_cycle['all_success']}")
        print(f"  全体成功率: {res_cycle['success_rate']:.6f} ({res_cycle['success_rate'] * 100:.4f}%)")
        print(f"  平均成功人数: {res_cycle['avg_success']:.2f} ± {res_cycle['std_success']:.2f}")
        print(f"  运行时间: {time_cycle:.2f}秒")

        # 计算改进比例
        if res_random['success_rate'] > 0:
            improvement = res_cycle['success_rate'] / res_random['success_rate']
            print(f"\n策略比较: 循环策略成功率是随机策略的 {improvement:.1f} 倍")
        else:
            print(f"\n策略比较: 随机策略成功率为0，循环策略具有绝对优势")

        return res_random, res_cycle

    def analyze_cycles(self, n_samples=1000):
        """分析循环长度分布，解释循环策略有效性"""
        cycle_lengths = []
        print(f"分析循环长度分布 (样本数: {n_samples})...")
        for i in range(n_samples):
            if (i + 1) % 200 == 0:
                print(f"进度: {i + 1}/{n_samples}")
            boxes = self.generate_boxes()
            visited = [False] * self.n
            cycles = []
            for start in range(self.n):
                if not visited[start]:
                    length = 0
                    current = start
                    while not visited[current]:
                        visited[current] = True
                        current = boxes[current]
                        length += 1
                    cycles.append(length)
            # 记录最长循环长度
            max_length = max(cycles)
            cycle_lengths.append(max_length)
        return cycle_lengths


def plot_results(res_rand, res_cyc):
    """绘制仿真结果的可视化图表"""
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))

    # 成功率对比柱状图
    strategies = ['随机策略', '循环策略']
    success_rates = [res_rand['success_rate'], res_cyc['success_rate']]
    bars = axs[0, 0].bar(strategies, success_rates, color=['skyblue', 'lightcoral'])
    axs[0, 0].set_ylabel('全体成功率')
    axs[0, 0].set_title('两种策略成功率对比')
    axs[0, 0].set_ylim(0, max(success_rates) * 1.2)
    # 添加数值标签
    for bar, rate in zip(bars, success_rates):
        axs[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.02,
                       f'{rate:.6f}', ha='center', fontweight='bold')

    # 成功人数分布对比
    axs[0, 1].hist(res_rand['success_list'], bins=50, alpha=0.7, label='随机策略', color='skyblue', density=True)
    axs[0, 1].hist(res_cyc['success_list'], bins=50, alpha=0.7, label='循环策略', color='lightcoral', density=True)
    axs[0, 1].set_xlabel('成功囚徒数量')
    axs[0, 1].set_ylabel('概率密度')
    axs[0, 1].set_title('成功囚徒数量分布')
    axs[0, 1].legend()
    axs[0, 1].grid(True, alpha=0.3)

    # 累积分布函数
    rand_sorted = np.sort(res_rand['success_list'])
    cyc_sorted = np.sort(res_cyc['success_list'])
    rand_cdf = np.arange(1, len(rand_sorted)+1) / len(rand_sorted)
    cyc_cdf = np.arange(1, len(cyc_sorted)+1) / len(cyc_sorted)
    axs[1, 0].plot(rand_sorted, rand_cdf, label='随机策略', color='skyblue', linewidth=2)
    axs[1, 0].plot(cyc_sorted, cyc_cdf, label='循环策略', color='lightcoral', linewidth=2)
    axs[1, 0].set_xlabel('成功囚徒数量')
    axs[1, 0].set_ylabel('累积概率')
    axs[1, 0].set_title('成功囚徒数量累积分布')
    axs[1, 0].legend()
    axs[1, 0].grid(True, alpha=0.3)

    # 统计表格
    axs[1, 1].axis('off')
    stats_text = f"""
统计结果对比

策略类型    全体成功率      平均成功数    标准差
随机策略    {res_rand['success_rate']:.6f}    {res_rand['avg_success']:.2f}         {res_rand['std_success']:.2f}
循环策略    {res_cyc['success_rate']:.6f}    {res_cyc['avg_success']:.2f}         {res_cyc['std_success']:.2f}

理论分析:
• 随机策略成功率 ≈ (1/2)^100 ≈ 0 (几乎不可能)
• 循环策略成功率 ≈ 0.31 (约31%)
• 关键洞察: 循环策略成功当且仅当最长循环 ≤ {50}
• 实际测量结果与理论预期相符
    """
    axs[1, 1].text(0.05, 0.95, stats_text, fontsize=10, va='top', ha='left', family='monospace')

    plt.tight_layout()
    plt.show()


def plot_cycle_analysis(simulator):
    """分析并绘制循环长度分布"""
    cycle_lengths = simulator.analyze_cycles(n_samples=5000)

    fig, axs = plt.subplots(1, 2, figsize=(15, 6))

    # 循环长度分布直方图
    axs[0].hist(cycle_lengths, bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
    axs[0].axvline(x=50, color='red', linestyle='--', label='临界值 (50)')
    axs[0].set_xlabel('最长循环长度')
    axs[0].set_ylabel('频次')
    axs[0].set_title('最长循环长度分布')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    # 成功概率随循环长度的变化
    success_prob = [np.mean(np.array(cycle_lengths) <= t) for t in range(1, 101)]
    axs[1].plot(range(1, 101), success_prob, color='darkgreen', linewidth=2)
    axs[1].axvline(x=50, color='red', linestyle='--', label='K=50')
    actual_rate = np.mean(np.array(cycle_lengths) <= 50)
    axs[1].axhline(y=actual_rate, color='orange', linestyle=':', label=f'实际成功率≈{actual_rate:.3f}')
    axs[1].set_xlabel('最大尝试次数 K')
    axs[1].set_ylabel('成功概率')
    axs[1].set_title('循环策略成功概率 vs 最大尝试次数')
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # 打印统计信息
    print(f"\n最长循环长度统计:")
    print(f"  平均值: {np.mean(cycle_lengths):.2f}")
    print(f"  中位数: {np.median(cycle_lengths):.2f}")
    print(f"  标准差: {np.std(cycle_lengths):.2f}")
    print(f"  最长循环 ≤ 50 的概率: {np.mean(np.array(cycle_lengths) <= 50):.6f}")

    return cycle_lengths


def parameter_analysis():
    """参数敏感性分析：测试不同的N和K值"""
    print("进行参数敏感性分析...")

    # 测试不同的参数组合
    test_cases = [
        (50, 25),   # N=50, K=25
        (100, 50),  # N=100, K=50 (标准情况)
        (100, 25),  # N=100, K=25 (更严格)
        (100, 75),  # N=100, K=75 (更宽松)
    ]

    results = []

    for n, k in test_cases:
        print(f"\n测试参数: N={n}, K={k}")
        simulator = PrisonerSimulator(n, k)

        # 减少模拟次数以节省时间
        res_rand = simulator.run_simulation(1000, 'random', verbose=False)
        res_cyc = simulator.run_simulation(1000, 'cycle', verbose=False)

        # 计算改进比例
        if res_rand['success_rate'] > 0:
            improvement = res_cyc['success_rate'] / res_rand['success_rate']
        else:
            improvement = float('inf')

        results.append({
            'n': n,
            'k': k,
            'k_ratio': k / n,
            'rand_rate': res_rand['success_rate'],
            'cyc_rate': res_cyc['success_rate'],
            'improvement': improvement
        })

        print(f"  随机策略成功率: {res_rand['success_rate']:.6f}")
        print(f"  循环策略成功率: {res_cyc['success_rate']:.6f}")
        if improvement != float('inf'):
            print(f"  改进比例: {improvement:.1f}倍")
        else:
            print(f"  改进比例: 无限大（随机策略成功率为0）")

    # 绘制参数分析结果
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))

    # 提取有效数据
    k_ratios = [r['k_ratio'] for r in results]
    rand_rates = [r['rand_rate'] for r in results]
    cyc_rates = [r['cyc_rate'] for r in results]
    finite_improvements = [r['improvement'] for r in results if r['improvement'] != float('inf')]
    finite_ratios = [r['k_ratio'] for r in results if r['improvement'] != float('inf')]

    # K/N 比例 vs 成功率
    axs[0].plot(k_ratios, rand_rates, 'o-', label='随机策略', color='skyblue', linewidth=2, markersize=8)
    axs[0].plot(k_ratios, cyc_rates, 's-', label='循环策略', color='lightcoral', linewidth=2, markersize=8)
    axs[0].set_xlabel('K/N 比例')
    axs[0].set_ylabel('成功率')
    axs[0].set_title('成功率 vs K/N 比例')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)
    axs[0].set_yscale('log')  # 使用对数刻度显示差异

    # 改进比例分析
    if finite_improvements and finite_ratios:
        axs[1].plot(finite_ratios, finite_improvements, 'o-', color='green', linewidth=2, markersize=8)
        axs[1].set_xlabel('K/N 比例')
        axs[1].set_ylabel('改进比例 (循环/随机)')
        axs[1].set_title('循环策略相对随机策略的改进比例')
        axs[1].grid(True, alpha=0.3)
    else:
        axs[1].text(0.5, 0.5, '无有限改进比例数据\n(随机策略成功率均为0)',
                    ha='center', va='center', transform=axs[1].transAxes, fontsize=12)
        axs[1].set_title('改进比例分析')

    plt.tight_layout()
    plt.show()

    return results


# 主程序执行
def main():
    print("=" * 60)
    print("           100囚徒抽签问题仿真分析")
    print("=" * 60)

    # 1. 基本仿真 (N=100, K=50)
    print("\n1. 基本仿真分析")
    simulator = PrisonerSimulator(100, 50)
    res_rand, res_cyc = simulator.compare_strategies(n_sims=10000)

    # 2. 绘制基本结果
    print("\n2. 生成可视化图表")
    plot_results(res_rand, res_cyc)

    # 3. 循环长度分析
    print("\n3. 循环长度分析")
    plot_cycle_analysis(simulator)

    # 4. 参数敏感性分析
    print("\n4. 参数敏感性分析")
    parameter_analysis()

    # 5. 理论计算验证
    print("\n5. 理论计算验证")
    # 理论成功率 = 1 - Σ(1/k) 从 k=K+1 到 N
    theoretical_rate = 1 - sum(1/k for k in range(51, 101))
    print(f"理论成功率: {theoretical_rate:.6f}")
    print(f"实验成功率: {res_cyc['success_rate']:.6f}")
    print(f"理论与实验差异: {abs(theoretical_rate - res_cyc['success_rate']):.6f}")

    print("\n" + "=" * 60)
    print("                   分析总结")
    print("=" * 60)
    print(f"""
主要发现:
1. 随机策略成功率: {res_rand['success_rate']:.2e}，几乎不可能成功
2. 循环策略成功率: {res_cyc['success_rate']:.3f}，约为{res_cyc['success_rate'] * 100:.1f}%
3. 循环策略的关键洞察：成功当且仅当最长循环长度 ≤ {simulator.k}
4. 理论成功率 = P(最长循环 ≤ {simulator.k}) ≈ {theoretical_rate:.3f}

数学原理:
- 随机策略：每个囚徒成功概率 = K/N = {simulator.k / simulator.n}，全体成功概率 = ({simulator.k / simulator.n})^N ≈ 0
- 循环策略：基于排列的循环结构，成功概率 = 1 - Σ(k=K+1 to N)[1/k] ≈ {theoretical_rate:.3f}
    """)


if __name__ == "__main__":
    main()