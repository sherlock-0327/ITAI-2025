import numpy as np
import matplotlib.pyplot as plt
import time
import seaborn as sns
from tqdm import tqdm
import math


class PrisonerProblemSimulator:
    def __init__(self, N=100, K=50, T=10000):
        """
        初始化囚犯问题模拟器

        参数:
        N: 囚犯数量 (默认100)
        K: 每人尝试次数 (默认50)
        T: 模拟轮次 (默认10000)
        """
        self.N = N
        self.K = K
        self.T = T
        self.results = {'random': [], 'cycle': []}
        self.cycle_lengths = []
        self.success_rates = {'random': 0, 'cycle': 0}

    def generate_boxes(self):
        """生成随机排列的盒子"""
        return np.random.permutation(self.N)

    def random_strategy(self, boxes):
        """
        随机搜索策略

        每个囚犯随机打开K个盒子寻找自己的编号
        返回: 所有囚犯是否都找到了自己的编号
        """
        for prisoner in range(self.N):
            # 随机选择K个盒子
            choices = np.random.choice(self.N, self.K, replace=False)
            # 检查是否找到自己的编号
            if prisoner not in boxes[choices]:
                return False
        return True

    def cycle_strategy(self, boxes):
        """
        循环搜索策略

        每个囚犯从自己编号的盒子开始，沿着盒子中的纸条跳转
        返回: 所有囚犯是否都找到了自己的编号
        """
        max_cycle_length = 0
        visited = np.zeros(self.N, dtype=bool)

        for prisoner in range(self.N):
            if visited[prisoner]:
                continue

            current = prisoner
            cycle_length = 0
            cycle_found = False

            # 沿着循环寻找
            for step in range(self.K):
                visited[current] = True
                next_box = boxes[current]

                # 如果找到自己的编号
                if next_box == prisoner:
                    cycle_length = step + 1
                    max_cycle_length = max(max_cycle_length, cycle_length)
                    cycle_found = True
                    break

                current = next_box

            # 如果在K步内没找到自己的编号
            if not cycle_found:
                return False, 0

        self.cycle_lengths.append(max_cycle_length)
        return True, max_cycle_length

    def run_simulation(self):
        """运行模拟"""
        print(f"开始模拟: N={self.N}, K={self.K}, T={self.T}次")

        # 进度条
        progress_bar = tqdm(total=self.T, desc="模拟进度")

        for trial in range(self.T):
            boxes = self.generate_boxes()

            # 随机策略
            random_result = self.random_strategy(boxes)
            self.results['random'].append(random_result)

            # 循环策略
            cycle_result, _ = self.cycle_strategy(boxes)
            self.results['cycle'].append(cycle_result)

            progress_bar.update(1)

        progress_bar.close()

        # 计算成功率
        self.success_rates['random'] = np.mean(self.results['random'])
        self.success_rates['cycle'] = np.mean(self.results['cycle'])

        print("\n模拟完成!")
        print(f"随机策略成功率: {self.success_rates['random'] * 100:.4f}%")
        print(f"循环策略成功率: {self.success_rates['cycle'] * 100:.4f}%")

    def theoretical_success_rate(self):
        """计算循环策略的理论成功率"""
        # 当最大循环长度不超过K时的概率
        total_prob = 0
        for L in range(self.K + 1, self.N + 1):
            # 计算最大循环长度恰好为L的概率
            prob = 1 / L
            # 减去更小循环长度的影响
            for i in range(L, self.N + 1):
                if i != L:
                    prob *= (1 - 1 / max(i, L))
            total_prob += prob

        # 理论成功率为1减去最大循环长度超过K的概率
        return 1 - total_prob

    def plot_results(self):
        """绘制结果图表"""
        plt.figure(figsize=(15, 10))

        # 成功率对比
        plt.subplot(2, 2, 1)
        strategies = ['随机策略', '循环策略']
        success_rates = [self.success_rates['random'], self.success_rates['cycle']]
        bars = plt.bar(strategies, success_rates, color=['skyblue', 'lightgreen'])
        plt.ylabel('成功率')
        plt.title('策略成功率对比')
        plt.ylim(0, 1)

        # 在柱子上添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.4f}', ha='center', va='bottom')

        # 循环长度分布
        plt.subplot(2, 2, 2)
        plt.hist(self.cycle_lengths, bins=range(1, self.N + 1), alpha=0.7, color='orange')
        plt.axvline(x=self.K, color='r', linestyle='--', label=f'K={self.K}')
        plt.xlabel('最大循环长度')
        plt.ylabel('频率')
        plt.title('循环策略最大循环长度分布')
        plt.legend()

        # 成功/失败分布
        plt.subplot(2, 2, 3)
        cycle_results = ['成功' if r else '失败' for r in self.results['cycle']]
        success_count = sum(1 for r in cycle_results if r == '成功')
        failure_count = len(cycle_results) - success_count
        plt.pie([success_count, failure_count], labels=['成功', '失败'],
                autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
        plt.title('循环策略成功/失败分布')

        # 理论成功率对比
        plt.subplot(2, 2, 4)
        theoretical_rate = self.theoretical_success_rate()
        plt.bar(['实际成功率', '理论成功率'],
                [self.success_rates['cycle'], theoretical_rate],
                color=['lightgreen', 'lightblue'])
        plt.ylabel('成功率')
        plt.title('循环策略实际与理论成功率对比')
        plt.ylim(0, 1)

        plt.tight_layout()
        plt.savefig('prisoner_problem_results.png')
        plt.show()

    def analyze_parameters(self):
        """分析不同参数对成功率的影响"""
        print("\n分析不同参数对成功率的影响...")

        # 固定K/N比例，改变N
        ratios = [0.3, 0.4, 0.5, 0.6, 0.7]
        N_values = [20, 40, 60, 80, 100]

        plt.figure(figsize=(15, 6))

        # 固定K/N比例
        plt.subplot(1, 2, 1)
        for ratio in ratios:
            success_rates = []
            for N in N_values:
                K = int(N * ratio)
                # 使用理论公式计算成功率
                prob = 0
                for L in range(K + 1, N + 1):
                    term = 1 / L
                    for i in range(L, N + 1):
                        if i != L:
                            term *= (1 - 1 / max(i, L))
                    prob += term
                success_rate = 1 - prob
                success_rates.append(success_rate)

            plt.plot(N_values, success_rates, 'o-', label=f'K/N={ratio}')

        plt.xlabel('囚犯数量 (N)')
        plt.ylabel('成功率')
        plt.title('固定K/N比例时的成功率变化')
        plt.legend()
        plt.grid(True)

        # 固定N，改变K
        plt.subplot(1, 2, 2)
        N_fixed = 100
        K_values = range(30, 81, 10)
        success_rates_fixed_N = []

        for K in K_values:
            prob = 0
            for L in range(K + 1, N_fixed + 1):
                term = 1 / L
                for i in range(L, N_fixed + 1):
                    if i != L:
                        term *= (1 - 1 / max(i, N_fixed))
                prob += term
            success_rate = 1 - prob
            success_rates_fixed_N.append(success_rate)

        plt.plot(K_values, success_rates_fixed_N, 's-', color='purple')
        plt.xlabel('尝试次数 (K)')
        plt.ylabel('成功率')
        plt.title(f'N={N_fixed}时不同K值的成功率变化')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('parameter_analysis.png')
        plt.show()

    def run(self):
        """运行完整模拟和分析"""
        start_time = time.time()
        self.run_simulation()
        end_time = time.time()

        print(f"\n模拟用时: {end_time - start_time:.2f}秒")

        # 绘制结果
        self.plot_results()

        # 参数分析
        self.analyze_parameters()

        # 输出理论值
        theoretical_rate = self.theoretical_success_rate()
        print(f"\n循环策略理论成功率: {theoretical_rate * 100:.4f}%")
        print(f"实际模拟成功率: {self.success_rates['cycle'] * 100:.4f}%")
        print(f"差异: {abs(self.success_rates['cycle'] - theoretical_rate) * 100:.4f}%")


# 主程序
if __name__ == "__main__":
    print("=" * 60)
    print("100囚犯抽签问题仿真分析")
    print("=" * 60)

    # 获取用户输入
    try:
        N = int(input("请输入囚犯数量N (默认100): ") or 100)
        K = int(input(f"请输入每人尝试次数K (默认{int(N / 2)}): ") or int(N / 2))
        T = int(input("请输入模拟轮次T (默认10000): ") or 10000)
    except ValueError:
        print("输入无效，使用默认参数")
        N, K, T = 100, 50, 10000

    # 验证参数
    if N < 2:
        print("N必须至少为2，使用默认值100")
        N = 100
    if K < 1 or K > N:
        K = max(1, min(N, int(N / 2)))
        print(f"K必须在1和{N}之间，设置为{K}")
    if T < 1:
        T = 10000
        print(f"T必须至少为1，设置为10000")

    # 创建模拟器并运行
    simulator = PrisonerProblemSimulator(N, K, T)
    simulator.run()