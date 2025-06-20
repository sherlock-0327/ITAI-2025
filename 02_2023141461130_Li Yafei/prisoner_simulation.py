import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple
import random
from tqdm.notebook import tqdm
import multiprocessing as mp

# 确保中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  

def generate_boxes(n: int) -> np.ndarray:
#盒子内编号随机实现
    return np.random.permutation(n) + 1

def random_strategy_vectorized(boxes: np.ndarray, prisoner_num: int, max_attempts: int) -> bool:
#向量化囚犯随即策略仿真
    n = len(boxes)
    attempts = np.random.choice(n, max_attempts, replace=False)
    return np.any(boxes[attempts] == prisoner_num)

def cycle_strategy(boxes: np.ndarray, prisoner_num: int, max_attempts: int) -> bool:
#仿真循环策略：囚犯将从自己的编号盒子开始
    current_box = prisoner_num - 1  # 从自己编号的盒子开始
    attempts = 0
    
    while attempts < max_attempts:
        if boxes[current_box] == prisoner_num:
            return True
        current_box = boxes[current_box] - 1
        attempts += 1
    
    return False

def simulate_round_vectorized(n: int, k: int, strategy: str) -> Tuple[bool, int]:
#向量化的单论模拟
    boxes = generate_boxes(n)
    if strategy == 'random':
        # 为所有囚犯一次性生成随机尝试
        attempts = np.array([np.random.choice(n, k, replace=False) for _ in range(n)])
        successes = np.array([np.any(boxes[attempts[i]] == i+1) for i in range(n)])
    else:
        # 循环策略仍然需要逐个处理，因为每个囚犯的尝试路径依赖于前一个盒子的结果
        successes = np.array([cycle_strategy(boxes, i+1, k) for i in range(n)])
    
    success_count = np.sum(successes)
    return success_count == n, success_count

def parallel_simulate(args):
#并行化实现函数
    n, k, strategy, trials = args
    results = {'success_rate': 0, 'success_counts': []}
    
    for _ in range(trials):
        success, count = simulate_round_vectorized(n, k, strategy)
        results['success_counts'].append(count)
        if success:
            results['success_rate'] += 1
    
    results['success_rate'] /= trials
    return results

def run_simulation_parallel(n: int = 100, k: int = 50, trials: int = 10000, n_processes: int = None) -> Tuple[dict, dict]:
#并行化多轮模拟
    if n_processes is None:
        n_processes = mp.cpu_count()  # 使用所有可用的CPU核心
    
    # 将总实验次数分配给每个进程
    trials_per_process = trials // n_processes
    remaining_trials = trials % n_processes
    
    # 准备并行处理参数
    random_args = [(n, k, 'random', trials_per_process + (1 if i < remaining_trials else 0)) 
                for i in range(n_processes)]
    cycle_args = [(n, k, 'cycle', trials_per_process + (1 if i < remaining_trials else 0)) 
                for i in range(n_processes)]
    
    # 创建进程池并执行并行计算
    with mp.Pool(processes=n_processes) as pool:
        random_results_list = pool.map(parallel_simulate, random_args)
        cycle_results_list = pool.map(parallel_simulate, cycle_args)
    
    # 合并结果
    random_results = {'success_rate': 0, 'success_counts': []}
    cycle_results = {'success_rate': 0, 'success_counts': []}
    
    for result in random_results_list:
        random_results['success_rate'] += result['success_rate'] * (len(result['success_counts']) / trials)
        random_results['success_counts'].extend(result['success_counts'])
    
    for result in cycle_results_list:
        cycle_results['success_rate'] += result['success_rate'] * (len(result['success_counts']) / trials)
        cycle_results['success_counts'].extend(result['success_counts'])
    
    return random_results, cycle_results

def plot_results(random_results: dict, cycle_results: dict, n: int, k: int, trials: int):
#可视化结果
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # 绘制成功率对比
    strategies = ['随机策略', '循环策略']
    success_rates = [random_results['success_rate'], cycle_results['success_rate']]
    
    ax1.bar(strategies, success_rates)
    ax1.set_title(f'策略成功率对比 (N={n}, K={k}, 实验次数={trials})')
    ax1.set_ylabel('成功率')
    for i, v in enumerate(success_rates):
        ax1.text(i, v, f'{v:.2%}', ha='center', va='bottom')
    
    # 绘制成功人数分布
    sns.histplot(data=cycle_results['success_counts'], bins=n+1, ax=ax2)
    ax2.set_title('循环策略成功人数分布')
    ax2.set_xlabel('成功找到自己编号的囚犯数量')
    ax2.set_ylabel('频次')
    
    plt.tight_layout()
    plt.show()

def analyze_parameters_parallel(trials: int = 1000, n_processes: int = None):
#并行化分析参数影响
    if n_processes is None:
        n_processes = mp.cpu_count()
    
    n_values = [50, 100, 200]
    k_values = [25, 50, 75]
    
    # 准备所有参数组合
    param_combinations = []
    for n in n_values:
        for k in k_values:
            if k <= n:  # 只处理有效组合
                param_combinations.append((n, k, 'cycle', trials))
    
    # 创建进程池并执行并行计算
    with mp.Pool(processes=n_processes) as pool:
        results = pool.map(parallel_simulate, param_combinations)
    
    # 绘制结果
    fig, axes = plt.subplots(len(n_values), len(k_values), figsize=(15, 12))
    fig.suptitle('不同参数组合下的循环策略成功率 (并行计算)', fontsize=16)
    
    result_index = 0
    for i, n in enumerate(n_values):
        for j, k in enumerate(k_values):
            if k > n:  # 跳过无效组合
                axes[i, j].text(0.5, 0.5, '无效参数', ha='center', va='center')
                continue
            
            success_rate = results[result_index]['success_rate']
            result_index += 1
            
            axes[i, j].bar(['循环策略'], [success_rate])
            axes[i, j].set_title(f'N={n}, K={k}\n成功率: {success_rate:.2%}')
            axes[i, j].set_ylim(0, 1)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # 设置随机种子
    np.random.seed(42)
    random.seed(42)
    
    # 运行基本模拟（使用并行处理）
    n, k, trials = 100, 50, 10000
    print(f"使用 {mp.cpu_count()} 个CPU核心进行并行计算")
    random_results, cycle_results = run_simulation_parallel(n, k, trials)
    plot_results(random_results, cycle_results, n, k, trials)
    
    # 分析参数影响（使用并行处理）
    analyze_parameters_parallel(trials=1000) 