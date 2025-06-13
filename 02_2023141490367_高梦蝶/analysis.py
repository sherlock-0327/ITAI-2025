import matplotlib.pyplot as plt
import numpy as np

def plot_success_rates(random_rate, loop_rate):
    plt.figure(figsize=(10,6))
    strategies = ['随机策略', '循环策略']
    rates = [random_rate, loop_rate]
    bars = plt.bar(strategies, rates, color=['#1f77b4', '#2ca02c'])
    
    plt.ylabel('成功率')
    plt.title('策略成功率对比')
    plt.ylim(0, 1)
    
    # 在柱子上方添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2%}',
                 ha='center', va='bottom')
    
    plt.savefig('strategy_comparison.png')
    plt.close()

def analyze_loop_lengths(loop_lengths):
    plt.figure(figsize=(10,6))
    plt.hist(loop_lengths, bins=20, color='#9467bd', edgecolor='black')
    plt.xlabel('循环链长度')
    plt.ylabel('出现频率')
    plt.title('循环链长度分布')
    plt.savefig('loop_length_distribution.png')
    plt.close()