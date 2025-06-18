import random
import numpy as np
import matplotlib.pyplot as plt

def generate_boxes(N):
    """生成随机排列的盒子内容"""
    return random.sample(range(1, N+1), N)

def random_strategy(boxes, prisoner_num, K):
    """随机策略：随机打开K个盒子"""
    opened = random.sample(range(len(boxes)), K)
    for box_idx in opened:
        if boxes[box_idx] == prisoner_num:
            return True
    return False

def cycle_strategy(boxes, prisoner_num, K):
    """循环策略：从自己的编号开始追踪循环"""
    current_box = prisoner_num - 1  # 转换为0-based索引
    steps = 0
    while steps < K:
        if boxes[current_box] == prisoner_num:
            return True
        current_box = boxes[current_box] - 1  # 跳转到下一个盒子
        steps += 1
    return False

def simulate(N, K, T, strategy):
    """模拟T轮实验"""
    successes = 0
    for _ in range(T):
        boxes = generate_boxes(N)
        all_success = True
        for prisoner in range(1, N+1):
            if strategy == 'random':
                found = random_strategy(boxes, prisoner, K)
            else:
                found = cycle_strategy(boxes, prisoner, K)
            
            if not found:
                all_success = False
                break
        
        if all_success:
            successes += 1
    
    return successes / T

def plot_success_distribution(N, K, T):
    """绘制循环策略的成功分布直方图"""
    cycle_lengths = []
    successes = 0
    
    for _ in range(T):
        boxes = generate_boxes(N)
        max_cycle = 0
        all_success = True
        
        # 计算所有循环的长度
        visited = [False] * N
        for i in range(N):
            if not visited[i]:
                cycle_len = 0
                current = i
                while not visited[current]:
                    visited[current] = True
                    current = boxes[current] - 1
                    cycle_len += 1
                if cycle_len > max_cycle:
                    max_cycle = cycle_len
        
        cycle_lengths.append(max_cycle)
        if max_cycle <= K:
            successes += 1
    
    # 绘制直方图
    plt.hist(cycle_lengths, bins=range(1, N+2), align='left', rwidth=0.8)
    plt.axvline(x=K, color='r', linestyle='--', label=f'K={K}')
    plt.xlabel('Maximum Cycle Length')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Maximum Cycle Lengths (N={N}, T={T})')
    plt.legend()
    plt.show()
    
    print(f"Success rate with cycle strategy: {successes/T:.4f}")

def main():
    # 默认参数
    N = 100
    K = 50
    T = 10000
    
    # 用户输入
    print("100 Prisoners Problem Simulation")
    N = int(input(f"Enter number of prisoners (default {N}): ") or N)
    K = int(input(f"Enter maximum attempts per prisoner (default {K}): ") or K)
    T = int(input(f"Enter number of trials (default {T}): ") or T)
    
    # 模拟两种策略
    print("\nSimulating random strategy...")
    random_success = simulate(N, K, T, 'random')
    print(f"Random strategy success rate: {random_success:.6f}")
    
    print("\nSimulating cycle strategy...")
    cycle_success = simulate(N, K, T, 'cycle')
    print(f"Cycle strategy success rate: {cycle_success:.6f}")
    
    # 绘制循环策略的成功分布
    print("\nPlotting cycle length distribution...")
    plot_success_distribution(N, K, T)
    
    # 理论计算
    theoretical_prob = sum(1/i for i in range(K+1, N+1))
    theoretical_prob = 1 - theoretical_prob
    print(f"\nTheoretical success probability for cycle strategy: {theoretical_prob:.6f}")

if __name__ == "__main__":
    main()