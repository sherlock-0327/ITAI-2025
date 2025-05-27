import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import argparse
import math
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置黑体，支持中文
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号

def random_strategy(boxes, N, K):
    """策略1：每个囚犯随机打开K个盒子，返回找到自己编号的囚犯数"""
    success_count = 0
    for prisoner in range(N):
        choices = np.random.choice(N, K, replace=False)  # 随机选择K个盒子
        if prisoner in boxes[choices]:  # 如果在这K个盒子中找到自己的编号
            success_count += 1
    return success_count

def loop_strategy(boxes, N, K):
    """策略2：循环策略，每个囚犯从自己编号的盒子开始，按纸条跳转，最多K次"""
    success_count = 0
    for prisoner in range(N):
        current = prisoner
        for _ in range(K):
            current = boxes[current]  # 跳转到下一个盒子
            if current == prisoner:   # 找到自己的编号
                success_count += 1
                break
    return success_count

def simulate_prisoners_problem(N=100, K=50, T=10000, verbose=False):
    """
    主仿真函数
    N: 囚犯数量
    K: 每人尝试次数
    T: 模拟轮数
    verbose: 是否输出每轮结果
    返回：两种策略的全体成功率和每轮成功人数列表
    """
    random_success_counts = []      # 随机策略每轮成功人数
    loop_success_counts = []        # 循环策略每轮成功人数
    random_success_rounds = []      # 随机策略每轮全体是否成功
    loop_success_rounds = []        # 循环策略每轮全体是否成功
    for i in tqdm(range(T), desc="Simulating"):
        boxes = np.random.permutation(N)  # 随机生成盒子排列
        r_count = random_strategy(boxes, N, K)
        l_count = loop_strategy(boxes, N, K)
        random_success_counts.append(r_count)
        loop_success_counts.append(l_count)
        # 每轮输出
        if verbose:
            print(f"第{i+1}轮：随机策略 {'成功' if r_count==N else '失败'}，循环策略 {'成功' if l_count==N else '失败'}")
        random_success_rounds.append(r_count==N)
        loop_success_rounds.append(l_count==N)
    # 计算全体成功率
    random_success_rate = np.mean(random_success_rounds)
    loop_success_rate = np.mean(loop_success_rounds)
    return random_success_rate, loop_success_rate, random_success_counts, loop_success_counts

def theoretical_loop_success(N, K):
    """理论上循环策略全体成功概率（排列循环理论）"""
    prob = 1 - sum(1/i for i in range(K+1, N+1))
    return prob

def get_input_or_default(prompt_text, default_value):
    """获取用户输入，若无输入则返回默认值"""
    try:
        value = input(f"{prompt_text}（默认{default_value}）：")
        if value.strip() == "":
            return default_value
        return int(value)
    except Exception:
        return default_value

if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, default=None, help='囚犯数量')
    parser.add_argument('--K', type=int, default=None, help='每人尝试次数')
    parser.add_argument('--T', type=int, default=None, help='模拟轮数')
    parser.add_argument('--verbose', action='store_true', help='是否输出每轮结果')
    args = parser.parse_args()

    # 支持命令行和交互式输入
    N = args.N if args.N is not None else get_input_or_default("请输入囚犯数量N", 100)
    K = args.K if args.K is not None else get_input_or_default("请输入每人尝试次数K", 50)
    T = args.T if args.T is not None else get_input_or_default("请输入模拟轮数T", 10000)
    verbose = args.verbose

    print(f"模拟参数：N={N}, K={K}, T={T}")

    # 运行仿真
    random_success, loop_success, random_counts, loop_counts = simulate_prisoners_problem(N, K, T, verbose=verbose)

    # 输出统计结果
    print(f"\n随机策略全体成功率: {random_success:.4f}")
    print(f"循环策略全体成功率: {loop_success:.4f}")
    print(f"循环策略理论全体成功率: {theoretical_loop_success(N, K):.4f}")