# 100 囚犯问题模拟实验
import random
import matplotlib.pyplot as plt

# 随机策略：每人随机翻 K 个盒子
def simulate_random_strategy(N=100, K=50):
    boxes = list(range(N))
    random.shuffle(boxes)
    for prisoner in range(N):
        opened = random.sample(range(N), K)
        if prisoner not in [boxes[i] for i in opened]:
            return False
    return True

# 循环策略：每人从自己编号的盒子开始
def simulate_loop_strategy(N=100, K=50):
    boxes = list(range(N))
    random.shuffle(boxes)
    for prisoner in range(N):
        current = prisoner
        for _ in range(K):
            current = boxes[current]
            if current == prisoner:
                break
        else:
            return False
    return True

# 多轮实验统计成功率
def run_experiment(strategy_func, T=10000, N=100, K=50):
    success = 0
    for _ in range(T):
        if strategy_func(N, K):
            success += 1
    return success / T

# 执行模拟对比
T = 10000
success_random = run_experiment(simulate_random_strategy, T)
success_loop = run_experiment(simulate_loop_strategy, T)

# 可视化对比
plt.bar(["Random", "Loop"], [success_random, success_loop], color=['red', 'green'])
plt.ylabel("Success Rate")
plt.title(f"100 Prisoners Problem Simulation ({T} Trials)")
plt.ylim(0, 1)
plt.grid(True, axis='y')
plt.savefig("E:\\prisoners_success_rate.png")

print(f"Random Strategy Success Rate: {success_random:.4f}")
print(f"Loop Strategy Success Rate: {success_loop:.4f}")
