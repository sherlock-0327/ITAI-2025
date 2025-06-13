import argparse
from simulation import simulate
from strategies import random_strategy, loop_strategy
from analysis import plot_success_rates, analyze_loop_lengths

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='囚犯抽签问题模拟器')
    parser.add_argument('--N', type=int, default=100, help='囚犯数量')
    parser.add_argument('--K', type=int, default=50, help='最大尝试次数')
    parser.add_argument('--T', type=int, default=10000, help='模拟轮次')
    
    args = parser.parse_args()
    
    # 运行两种策略的模拟
    random_rate = simulate(args.T, args.N, args.K, random_strategy)
    loop_rate = simulate(args.T, args.N, args.K, loop_strategy)
    
    # 生成对比图表
    plot_success_rates(random_rate, loop_rate)
    
    print(f'随机策略成功率: {random_rate:.2%}')
    print(f'循环策略成功率: {loop_rate:.2%}')
    print('对比图表已保存为 strategy_comparison.png')