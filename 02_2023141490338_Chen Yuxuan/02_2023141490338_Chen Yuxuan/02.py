import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def simulate_prisoners(N=100, K=50, T=10000):
    # 存储结果
    random_successes = np.zeros(T, dtype=bool)
    cycle_successes = np.zeros(T, dtype=bool)
    random_counts = np.zeros(T, dtype=int)
    cycle_counts = np.zeros(T, dtype=int)
    max_cycle_lengths = np.zeros(T, dtype=int)
    
    for trial in tqdm(range(T)):
        # 生成随机排列
        boxes = np.random.permutation(N)
        
        # 随机策略
        random_success = np.zeros(N, dtype=bool)
        for prisoner in range(N):
            # 随机选择K个盒子
            choices = np.random.choice(N, K, replace=False)
            if prisoner in boxes[choices]:
                random_success[prisoner] = True
        random_successes[trial] = np.all(random_success)
        random_counts[trial] = np.sum(random_success)
        
        # 循环策略
        cycle_success = np.zeros(N, dtype=bool)
        visited = np.zeros(N, dtype=bool)
        max_cycle_length = 0
        
        for prisoner in range(N):
            if visited[prisoner]:
                continue
                
            current = prisoner
            cycle = []
            
            for _ in range(K):
                visited[current] = True
                cycle.append(current)
                if boxes[current] == prisoner:
                    cycle_success[prisoner] = True
                    break
                current = boxes[current]
            else:
                # 超过K次未找到
                pass
                
            if len(cycle) > max_cycle_length:
                max_cycle_length = len(cycle)
        
        cycle_successes[trial] = np.all(cycle_success)
        cycle_counts[trial] = np.sum(cycle_success)
        max_cycle_lengths[trial] = max_cycle_length
    
    return {
        'random_successes': random_successes,
        'cycle_successes': cycle_successes,
        'random_counts': random_counts,
        'cycle_counts': cycle_counts,
        'max_cycle_lengths': max_cycle_lengths
    }

def plot_results(results, N=100, K=50, T=10000):
    # 成功率统计
    random_success_rate = np.mean(results['random_successes'])
    cycle_success_rate = np.mean(results['cycle_successes'])
    
    print(f"随机策略成功率: {random_success_rate:.4f}")
    print(f"循环策略成功率: {cycle_success_rate:.4f}")
    print(f"理论循环策略成功率: {1 - sum(1/i for i in range(K+1, N+1)):.4f}")
    
    # 成功率柱状图
    plt.figure(figsize=(10, 6))
    plt.bar(['随机策略', '循环策略'], [random_success_rate, cycle_success_rate], color=['blue', 'green'])
    plt.axhline(y=1 - sum(1/i for i in range(K+1, N+1)), color='r', linestyle='--', label='理论值')
    plt.title(f'策略成功率比较 (N={N}, K={K}, T={T})')
    plt.ylabel('成功率')
    plt.ylim(0, 0.35)
    plt.legend()
    plt.savefig('success_rate_comparison.png')
    plt.show()
    
    # 成功人数分布
    plt.figure(figsize=(12, 6))
    plt.hist(results['random_counts'], bins=np.arange(0, N+5, 5), alpha=0.7, label='随机策略')
    plt.hist(results['cycle_counts'], bins=np.arange(0, N+5, 5), alpha=0.7, label='循环策略')
    plt.axvline(x=N, color='r', linestyle='--', label='全员成功')
    plt.title(f'成功人数分布 (N={N}, K={K}, T={T})')
    plt.xlabel('成功人数')
    plt.ylabel('频数')
    plt.legend()
    plt.savefig('success_count_distribution.png')
    plt.show()
    
    # 循环长度分布
    plt.figure(figsize=(10, 6))
    bins = np.arange(0, N+10, 10)
    plt.hist(results['max_cycle_lengths'], bins=bins, alpha=0.7)
    plt.axvline(x=K, color='r', linestyle='--', label=f'K={K}')
    plt.title(f'最大循环长度分布 (N={N}, T={T})')
    plt.xlabel('最大循环长度')
    plt.ylabel('频数')
    plt.legend()
    plt.savefig('max_cycle_length_distribution.png')
    plt.show()

# 主实验
results_100_50 = simulate_prisoners(N=100, K=50, T=10000)
plot_results(results_100_50, N=100, K=50, T=10000)

# 扩展实验：N=50, K=25
results_50_25 = simulate_prisoners(N=50, K=25, T=10000)
plot_results(results_50_25, N=50, K=25, T=10000)
