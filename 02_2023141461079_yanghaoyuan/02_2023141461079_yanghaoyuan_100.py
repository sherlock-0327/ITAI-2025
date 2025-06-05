import numpy as np
import matplotlib.pyplot as plt

def random_search_strategy(N, K, T):
    """
    执行随机搜索策略的仿真。
    
    参数:
    N -- 盒子（和囚犯）的数量
    K -- 每个囚犯允许尝试的次数
    T -- 仿真轮次
    
    返回:
    成功率（在T轮仿真中所有囚犯都在K次尝试内找到自己编号的比率）
    """
    success_count = 0
    for _ in range(T):
        # 随机生成盒子的排列
        boxes = np.random.permutation(N)
        found = np.zeros(N, dtype=bool)
        for prisoner in range(N):
            attempts = 0
            while attempts < K:
                # 随机选择一个盒子
                box = np.random.randint(N)
                if box == prisoner:
                    found[prisoner] = True
                    break
                attempts += 1
        # 如果所有囚犯都找到了自己的编号，则认为这一轮成功
        if np.all(found):
            success_count += 1
    return success_count / T

def loop_strategy(N, K, T):
    """
    执行循环策略的仿真。
    
    参数:
    N -- 盒子（和囚犯）的数量
    K -- 每个囚犯允许尝试的次数
    T -- 仿真轮次
    
    返回:
    成功率（在T轮仿真中所有囚犯都在K次尝试内找到自己编号的比率）
    """
    success_count = 0
    for _ in range(T):
        # 随机生成盒子的排列
        boxes = np.random.permutation(N)
        found = np.zeros(N, dtype=bool)
        for prisoner in range(N):
            current_box = prisoner
            attempts = 0
            while attempts < K:
                # 根据盒内的数字跳转到相应编号的盒子
                next_box = boxes[current_box]
                if next_box == prisoner:
                    found[prisoner] = True
                    break
                current_box = next_box
                attempts += 1
        # 如果所有囚犯都找到了自己的编号，则认为这一轮成功
        if np.all(found):
            success_count += 1
    return success_count / T

def main():
    N = 50  # 盒子（和囚犯）的数量
    K = 25   # 每个囚犯允许尝试的次数
    T = 1000 # 仿真轮次

    # 执行随机搜索策略的仿真
    random_success_rate = random_search_strategy(N, K, T)
    print(f"Random Search Strategy Success Rate: {random_success_rate:.2%}")

    # 执行循环策略的仿真
    loop_success_rate = loop_strategy(N, K, T)
    print(f"Loop Strategy Success Rate: {loop_success_rate:.2%}")

    # 绘制成功率对比图
    strategies = ['Random Search', 'Loop']
    success_rates = [random_success_rate, loop_success_rate]

    plt.bar(strategies, success_rates, color=['blue', 'green'])
    plt.xlabel('Strategy')
    plt.ylabel('Success Rate')
    plt.title('Comparison of Success Rates')
    plt.show()

if __name__ == "__main__":
    main()
