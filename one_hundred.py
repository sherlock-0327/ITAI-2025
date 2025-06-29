import numpy as np
import matplotlib.pyplot as plt
import time
from collections import Counter


class PrisonerSimulator:
    def __init__(self, N=100, K=50):
        self.N = N
        self.K = K

    def generate_boxes(self):
        """生成随机盒子配置"""
        return np.random.permutation(self.N)

    def random_strategy(self, boxes):
        """随机开箱策略"""
        successes = 0
        for prisoner in range(self.N):
            found = False
            choices = np.random.choice(self.N, self.K, replace=False)
            for choice in choices:
                if boxes[choice] == prisoner:
                    found = True
                    break
            if found:
                successes += 1
        return successes == self.N

    def loop_strategy(self, boxes):
        """循环策略"""
        successes = 0
        for prisoner in range(self.N):
            found = False
            next_box = prisoner
            for _ in range(self.K):
                if boxes[next_box] == prisoner:
                    found = True
                    break
                next_box = boxes[next_box]
            if found:
                successes += 1
        return successes == self.N

    def simulate(self, T=10000, strategy='loop'):
        """运行模拟"""
        results = []
        strategy_fn = self.loop_strategy if strategy == 'loop' else self.random_strategy

        for _ in range(T):
            boxes = self.generate_boxes()
            success = strategy_fn(boxes)
            results.append(success)

        success_rate = sum(results) / T
        return results, success_rate

    def run_experiments(self, T=10000):
        """对比两种策略"""
        print(f"Simulating {T} trials...")

        # 循环策略
        start = time.time()
        loop_results, loop_rate = self.simulate(T, 'loop')
        loop_time = time.time() - start

        # 随机策略
        start = time.time()
        random_results, random_rate = self.simulate(T, 'random')
        random_time = time.time() - start

        # 打印结果
        print(f"Loop strategy success rate: {loop_rate:.4f} (Time: {loop_time:.2f}s)")
        print(f"Random strategy success rate: {random_rate:.4f} (Time: {random_time:.2f}s)")

        # 绘制成功率比较
        plt.bar(['Loop Strategy', 'Random Strategy'], [loop_rate, random_rate])
        plt.ylabel('Success Rate')
        plt.title('Prisoner Problem Strategy Comparison')
        plt.ylim(0, 0.4)
        plt.savefig('prisoners_comparison.png')
        plt.show()

        # 循环长度分布
        self.loop_length_distribution(T)

    def loop_length_distribution(self, T):
        """分析循环长度分布"""
        loop_lengths = []
        for _ in range(T):
            boxes = self.generate_boxes()
            visited = [False] * self.N
            for i in range(self.N):
                if not visited[i]:
                    count = 0
                    current = i
                    while not visited[current]:
                        visited[current] = True
                        count += 1
                        current = boxes[current]
                    loop_lengths.append(count)

        # 绘制分布图
        plt.hist(loop_lengths, bins=range(1, max(loop_lengths) + 2), alpha=0.7)
        plt.xlabel('Loop Length')
        plt.ylabel('Frequency')
        plt.title('Distribution of Loop Lengths')
        plt.savefig('loop_distribution.png')
        plt.show()


def main():
    print("100 Prisoners Problem Simulator")

    # 获取参数
    try:
        N = int(input("Number of prisoners (default 100): ") or 100)
        K = int(input("Number of attempts (default 50): ") or 50)
        T = int(input("Simulation trials (default 10000): ") or 10000)
    except ValueError:
        print("Invalid input. Using defaults.")
        N, K, T = 100, 50, 10000

    simulator = PrisonerSimulator(N, K)
    simulator.run_experiments(T)


if __name__ == "__main__":
    main()