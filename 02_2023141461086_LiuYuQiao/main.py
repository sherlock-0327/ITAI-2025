import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import seaborn as sns

class PrisonerSimulation:
    def __init__(self, N=100, K=50, T=10000):
        """
        初始化囚徒仿真实验
        
        参数:
        N: 囚徒数量 (默认100)
        K: 每个囚徒允许尝试的次数 (默认50)
        T: 实验轮数 (默认10000)
        """
        self.N = N
        self.K = K
        self.T = T
        self.strategy1_success = np.zeros(T, dtype=bool)
        self.strategy2_success = np.zeros(T, dtype=bool)
        self.strategy2_loop_lengths = []
        
    def generate_boxes(self):
        """生成随机盒子配置"""
        return np.random.permutation(self.N)
    
    def strategy1_random(self, boxes):
        """策略1: 每个囚徒随机打开K个盒子"""
        for prisoner in range(self.N):
            opened = np.random.choice(self.N, size=self.K, replace=False)
            if prisoner not in boxes[opened]:
                return False
        return True
    
    def strategy2_loop(self, boxes):
        """策略2: 每个囚徒跟随循环策略"""
        loop_lengths = []
        visited = np.zeros(self.N, dtype=bool)
        
        for prisoner in range(self.N):
            if visited[prisoner]:
                continue
                
            current = prisoner
            loop_length = 0
            loop_prisoners = []
            
            while not visited[current]:
                visited[current] = True
                loop_prisoners.append(current)
                current = boxes[current]
                loop_length += 1
                
            loop_lengths.append(loop_length)
            # 检查这个循环中是否有囚徒会失败
            if loop_length > self.K:
                # 记录所有受影响的囚徒
                for p in loop_prisoners:
                    if p < self.N:  # 确保我们只考虑实际囚徒
                        pass
                return False, loop_lengths
        
        return True, loop_lengths
    
    def run_simulation(self):
        """运行仿真实验"""
        for t in tqdm(range(self.T), desc="Running simulation"):
            boxes = self.generate_boxes()
            
            # 策略1
            self.strategy1_success[t] = self.strategy1_random(boxes)
            
            # 策略2
            success, loop_lengths = self.strategy2_loop(boxes)
            self.strategy2_success[t] = success
            self.strategy2_loop_lengths.extend(loop_lengths)
    
    def report_results(self):
        """生成结果报告"""
        # 计算成功率
        strategy1_rate = np.mean(self.strategy1_success)
        strategy2_rate = np.mean(self.strategy2_success)
        
        print(f"仿真结果 (N={self.N}, K={self.K}, T={self.T}):")
        print(f"策略1 (随机) 成功率: {strategy1_rate:.4f} ({int(strategy1_rate * self.T)}/{self.T})")
        print(f"策略2 (循环) 成功率: {strategy2_rate:.4f} ({int(strategy2_rate * self.T)}/{self.T})")
        
        # Plot success distribution for Strategy 2
        plt.figure(figsize=(12, 6))
        
        # Loop length distribution
        plt.subplot(1, 2, 1)
        max_loop = min(max(self.strategy2_loop_lengths), 100)
        bins = np.arange(0.5, max_loop + 1.5, 1)
        plt.hist(self.strategy2_loop_lengths, bins=bins, density=True, alpha=0.7)
        plt.axvline(x=self.K, color='r', linestyle='--', label=f'K={self.K}')
        plt.xlabel('Loop Length')
        plt.ylabel('Probability Density')
        plt.title('Distribution of Loop Lengths')
        plt.legend()
        
        # Success rate comparison
        plt.subplot(1, 2, 2)
        plt.bar(['Random Strategy', 'Loop Strategy'], [strategy1_rate, strategy2_rate], alpha=0.7)
        plt.ylabel('Success Rate')
        plt.title('Strategy Comparison')
        plt.ylim(0, 1)
        
        plt.tight_layout()
        plt.show()
        
        # 显示一些理论解释
        if self.N == 100 and self.K == 50:
            theoretical_prob = 1 - np.log(2)
            print(f"\n理论解释:")
            print(f"循环策略的理论成功率约为: {theoretical_prob:.4f}")
            print("循环策略更优的原因是:")
            print("1. 所有囚徒成功当且仅当所有循环长度 ≤ K")
            print("2. 随机排列中长循环的概率较低 (约1 - ln2 ≈ 30%)")
            print("3. 随机策略的成功概率约为 (K/N)^N ≈ 7.9e-31 (极低)")

def extended_analysis():
    """扩展分析: 不同N和K对成功率的影响"""
    # 固定K=50, 改变N
    N_values = [50, 100, 200, 500]
    K_fixed = 50
    results_N = []
    
    for N in N_values:
        sim = PrisonerSimulation(N=N, K=min(K_fixed, N//2), T=1000)
        sim.run_simulation()
        rate = np.mean(sim.strategy2_success)
        results_N.append(rate)
        print(f"N={N}, K={min(K_fixed, N//2)}: 成功率={rate:.4f}")
    
    # 固定N=100, 改变K
    N_fixed = 100
    K_values = [30, 40, 50, 60, 70]
    results_K = []
    
    for K in K_values:
        sim = PrisonerSimulation(N=N_fixed, K=K, T=1000)
        sim.run_simulation()
        rate = np.mean(sim.strategy2_success)
        results_K.append(rate)
        print(f"N={N_fixed}, K={K}: 成功率={rate:.4f}")
    
    # Plot results
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(N_values, results_N, 'o-')
    plt.xlabel('N (Number of prisoners)')
    plt.ylabel('Success rate')
    plt.title(f'Success Rate vs N (Fixed K={K_fixed})')
    
    plt.subplot(1, 2, 2)
    plt.plot(K_values, results_K, 'o-')
    plt.xlabel('K (Number of attempts)')
    plt.ylabel('Success rate')
    plt.title(f'Success Rate vs K (Fixed N={N_fixed})')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 主仿真实验
    sim = PrisonerSimulation(N=100, K=50, T=10000)
    sim.run_simulation()
    sim.report_results()
    
    # 扩展分析
    print("\n进行扩展分析...")
    extended_analysis()