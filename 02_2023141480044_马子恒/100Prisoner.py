import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import defaultdict
import time
from typing import List, Tuple, Dict
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class PrisonerBoxProblem:
    """100囚犯抽签问题仿真类"""

    def __init__(self, n_prisoners: int = 100, max_attempts: int = 50):
        """
        初始化参数

        Args:
            n_prisoners: 囚犯数量
            max_attempts: 每个囚犯最多尝试次数
        """
        self.n_prisoners = n_prisoners
        self.max_attempts = max_attempts

    def generate_box_arrangement(self) -> np.ndarray:
        """
        生成随机的盒子编号排列

        Returns:
            长度为n_prisoners的数组，表示每个盒子内的编号
        """
        return np.random.permutation(self.n_prisoners) + 1

    def random_strategy(self, boxes: np.ndarray, prisoner_id: int) -> bool:
        """
        随机搜索策略

        Args:
            boxes: 盒子排列
            prisoner_id: 囚犯编号 (1-based)

        Returns:
            是否成功找到自己的编号
        """
        # 随机选择max_attempts个不重复的盒子
        box_indices = np.random.choice(self.n_prisoners, self.max_attempts, replace=False)

        for box_idx in box_indices:
            if boxes[box_idx] == prisoner_id:
                return True
        return False

    def cycle_strategy(self, boxes: np.ndarray, prisoner_id: int) -> bool:
        """
        循环策略（跟随链条策略）

        Args:
            boxes: 盒子排列
            prisoner_id: 囚犯编号 (1-based)

        Returns:
            是否成功找到自己的编号
        """
        current_box = prisoner_id - 1  # 转换为0-based索引

        for _ in range(self.max_attempts):
            if boxes[current_box] == prisoner_id:
                return True
            # 跳转到下一个盒子
            current_box = boxes[current_box] - 1  # 转换为0-based索引

        return False

    def simulate_single_experiment(self, strategy: str) -> Tuple[bool, int]:
        """
        模拟单次实验

        Args:
            strategy: 'random' 或 'cycle'

        Returns:
            (是否全体成功, 成功的囚犯数量)
        """
        boxes = self.generate_box_arrangement()
        success_count = 0

        for prisoner_id in range(1, self.n_prisoners + 1):
            if strategy == 'random':
                if self.random_strategy(boxes, prisoner_id):
                    success_count += 1
            elif strategy == 'cycle':
                if self.cycle_strategy(boxes, prisoner_id):
                    success_count += 1
            else:
                raise ValueError("Strategy must be 'random' or 'cycle'")

        all_success = (success_count == self.n_prisoners)
        return all_success, success_count

    def run_simulation(self, n_trials: int, strategy: str) -> Dict:
        """
        运行多次仿真实验

        Args:
            n_trials: 实验次数
            strategy: 策略类型

        Returns:
            实验结果字典
        """
        results = {
            'all_success': [],
            'success_counts': [],
            'success_rate': 0.0
        }

        print(f"开始运行 {strategy} 策略，共 {n_trials} 次实验...")
        start_time = time.time()

        for trial in range(n_trials):
            all_success, success_count = self.simulate_single_experiment(strategy)
            results['all_success'].append(all_success)
            results['success_counts'].append(success_count)

            if (trial + 1) % (n_trials // 10) == 0:
                print(f"进度: {(trial + 1) / n_trials * 100:.1f}%")

        results['success_rate'] = np.mean(results['all_success'])
        end_time = time.time()

        print(f"{strategy} 策略完成，用时 {end_time - start_time:.2f} 秒")
        print(f"全体成功率: {results['success_rate']:.6f}")

        return results

    def theoretical_success_rate(self) -> float:
        """
        计算循环策略的理论成功率
        基于调和级数：P = 1 - H_n + H_k，其中H_n是第n个调和数
        对于n=100, k=50的情况，理论成功率约为30.685%
        """
        harmonic_n = sum(1 / i for i in range(self.max_attempts + 1, self.n_prisoners + 1))
        return 1 - harmonic_n

    def analyze_cycle_lengths(self, n_samples: int = 1000) -> List[int]:
        """
        分析循环长度分布

        Args:
            n_samples: 采样次数

        Returns:
            最长循环长度列表
        """
        max_cycle_lengths = []

        for _ in range(n_samples):
            boxes = self.generate_box_arrangement()
            visited = [False] * self.n_prisoners
            cycle_lengths = []

            for start in range(self.n_prisoners):
                if not visited[start]:
                    # 找到从这个位置开始的循环
                    cycle_length = 0
                    current = start

                    while not visited[current]:
                        visited[current] = True
                        current = boxes[current] - 1  # 转换为0-based
                        cycle_length += 1

                    cycle_lengths.append(cycle_length)

            max_cycle_lengths.append(max(cycle_lengths))

        return max_cycle_lengths


def plot_results(random_results: Dict, cycle_results: Dict,
                 cycle_lengths: List[int], n_prisoners: int, max_attempts: int):
    """绘制分析结果图表"""

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # 1. 成功率对比
    strategies = ['随机策略', '循环策略']
    success_rates = [random_results['success_rate'], cycle_results['success_rate']]

    bars = ax1.bar(strategies, success_rates, color=['red', 'green'], alpha=0.7)
    ax1.set_ylabel('全体成功率')
    ax1.set_title('两种策略成功率对比')
    ax1.set_ylim(0, max(success_rates) * 1.2)

    # 添加数值标签
    for bar, rate in zip(bars, success_rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{rate:.6f}', ha='center', va='bottom')

    # 2. 随机策略成功人数分布
    ax2.hist(random_results['success_counts'], bins=30, alpha=0.7, color='red',
             density=True, label='随机策略')
    ax2.set_xlabel('成功囚犯数量')
    ax2.set_ylabel('概率密度')
    ax2.set_title('随机策略成功人数分布')
    ax2.axvline(np.mean(random_results['success_counts']),
                color='darkred', linestyle='--', label=f'均值: {np.mean(random_results["success_counts"]):.1f}')
    ax2.legend()

    # 3. 循环策略成功人数分布
    success_counts_cycle = np.array(cycle_results['success_counts'])
    unique_counts, count_frequencies = np.unique(success_counts_cycle, return_counts=True)

    ax3.bar(unique_counts, count_frequencies / len(success_counts_cycle),
            alpha=0.7, color='green', width=0.8)
    ax3.set_xlabel('成功囚犯数量')
    ax3.set_ylabel('频率')
    ax3.set_title('循环策略成功人数分布')

    # 标注全体成功的情况
    if n_prisoners in unique_counts:
        idx = np.where(unique_counts == n_prisoners)[0][0]
        ax3.bar(n_prisoners, count_frequencies[idx] / len(success_counts_cycle),
                color='darkgreen', alpha=0.8, width=0.8)
        ax3.text(n_prisoners, count_frequencies[idx] / len(success_counts_cycle) + 0.01,
                 f'全体成功\n{count_frequencies[idx] / len(success_counts_cycle):.4f}',
                 ha='center', va='bottom', fontweight='bold')

    # 4. 最长循环长度分布
    ax4.hist(cycle_lengths, bins=range(1, max(cycle_lengths) + 2),
             alpha=0.7, color='blue', density=True)
    ax4.axvline(max_attempts, color='red', linestyle='--',
                label=f'最大尝试次数: {max_attempts}')
    ax4.set_xlabel('最长循环长度')
    ax4.set_ylabel('概率密度')
    ax4.set_title('随机排列中最长循环长度分布')
    ax4.legend()

    # 标注成功区域
    ax4.axvspan(1, max_attempts, alpha=0.2, color='green', label='成功区域')
    ax4.legend()

    plt.tight_layout()
    plt.show()


def main():
    """主程序"""
    print("=" * 60)
    print("100囚犯抽签问题仿真程序")
    print("=" * 60)

    # 参数设置
    N_PRISONERS = 100
    MAX_ATTEMPTS = 50
    N_TRIALS = 10000

    # 创建问题实例
    problem = PrisonerBoxProblem(N_PRISONERS, MAX_ATTEMPTS)

    # 运行仿真
    print(f"\n问题参数:")
    print(f"囚犯数量: {N_PRISONERS}")
    print(f"每人最多尝试次数: {MAX_ATTEMPTS}")
    print(f"仿真次数: {N_TRIALS}")
    print()

    # 随机策略仿真
    random_results = problem.run_simulation(N_TRIALS, 'random')

    # 循环策略仿真
    cycle_results = problem.run_simulation(N_TRIALS, 'cycle')

    # 理论成功率
    theoretical_rate = problem.theoretical_success_rate()
    print(f"\n循环策略理论成功率: {theoretical_rate:.6f}")
    print(f"循环策略仿真成功率: {cycle_results['success_rate']:.6f}")
    print(f"理论与仿真差异: {abs(theoretical_rate - cycle_results['success_rate']):.6f}")

    # 分析循环长度
    print("\n分析循环长度分布...")
    cycle_lengths = problem.analyze_cycle_lengths(1000)

    # 绘制结果
    plot_results(random_results, cycle_results, cycle_lengths, N_PRISONERS, MAX_ATTEMPTS)

    # 输出详细统计
    print("\n" + "=" * 60)
    print("详细统计结果")
    print("=" * 60)

    print(f"\n随机策略:")
    print(f"  全体成功率: {random_results['success_rate']:.6f}")
    print(f"  平均成功人数: {np.mean(random_results['success_counts']):.2f}")
    print(f"  成功人数标准差: {np.std(random_results['success_counts']):.2f}")

    print(f"\n循环策略:")
    print(f"  全体成功率: {cycle_results['success_rate']:.6f}")
    print(f"  平均成功人数: {np.mean(cycle_results['success_counts']):.2f}")
    print(f"  成功人数标准差: {np.std(cycle_results['success_counts']):.2f}")

    print(f"\n循环长度分析:")
    print(f"  平均最长循环长度: {np.mean(cycle_lengths):.2f}")
    print(f"  最长循环长度超过{MAX_ATTEMPTS}的概率: {np.mean(np.array(cycle_lengths) > MAX_ATTEMPTS):.6f}")

    # 扩展分析：不同参数下的成功率
    print(f"\n扩展分析：不同参数下的循环策略成功率")
    print("-" * 40)

    test_params = [(50, 25), (60, 30), (80, 40), (100, 50), (120, 60)]

    for n, k in test_params:
        test_problem = PrisonerBoxProblem(n, k)
        test_results = test_problem.run_simulation(1000, 'cycle')
        theoretical = test_problem.theoretical_success_rate()
        print(f"N={n:3d}, K={k:2d}: 仿真={test_results['success_rate']:.4f}, "
              f"理论={theoretical:.4f}, 差异={abs(theoretical - test_results['success_rate']):.4f}")


if __name__ == "__main__":
    main()
