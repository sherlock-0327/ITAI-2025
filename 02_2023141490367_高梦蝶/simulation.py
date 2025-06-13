import numpy as np
from strategies import random_strategy, loop_strategy

def run_experiment(N, K, strategy):
    boxes = np.random.permutation(N) + 1
    for prisoner in range(1, N+1):
        if not strategy(prisoner, boxes, K):
            return False
    return True

def simulate(T, N=100, K=50, strategy=loop_strategy):
    successes = 0
    for _ in range(T):
        if run_experiment(N, K, strategy):
            successes += 1
    return successes / T

if __name__ == '__main__':
    # 示例运行参数
    success_rate = simulate(T=10000)
    print(f'成功率: {success_rate:.2%}')