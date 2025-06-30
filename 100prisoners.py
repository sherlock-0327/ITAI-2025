import random
import matplotlib.pyplot as plt
from collections import Counter

def simulate_strategy_random(N, K):
    """模拟随机搜索策略"""
    boxes = list(range(1, N+1))
    random.shuffle(boxes)
    
    for prisoner in range(1, N+1):
        chosen_boxes = random.sample(range(1, N+1), K)
        found = False
        for box in chosen_boxes:
            if boxes[box-1] == prisoner:
                found = True
                break
        if not found:
            return False
    return True

def simulate_strategy_loop(N, K):
    """模拟循环搜索策略"""
    boxes = list(range(1, N+1))
    random.shuffle(boxes)
    
    for prisoner in range(1, N+1):
        current_box = prisoner
        found = False
        for _ in range(K):
            if boxes[current_box-1] == prisoner:
                found = True
                break
            current_box = boxes[current_box-1]
        if not found:
            return False
    return True

def calculate_theoretical_success_rate(N):
    """计算循环策略的理论成功率"""
    return 1 - sum(1/i for i in range(N//2 + 1, N+1))

def run_simulation(N=100, K=50, T=10000):
    """运行模拟并比较两种策略"""
    random_success_count = 0
    loop_success_count = 0
    loop_success_distribution = []
    
    print(f"开始模拟: 囚犯数量={N}, 尝试次数={K}, 模拟轮次={T}")
    print("轮次 | 随机策略结果 | 循环策略结果")
    print("-" * 35)
    
    for i in range(T):
        # 策略1：随机搜索
        random_success = simulate_strategy_random(N, K)
        if random_success:
            random_success_count += 1
        
        # 策略2：循环搜索
        loop_success = simulate_strategy_loop(N, K)
        if loop_success:
            loop_success_count += 1
        
        # 输出每轮结果
        if i < 10 or i % 1000 == 0 or i == T-1:  # 只输出前10轮、中间每1000轮和最后一轮
            print(f"{i+1:4d} | {'成功' if random_success else '失败':^12s} | {'成功' if loop_success else '失败':^12s}")
    
    random_success_rate = random_success_count / T
    loop_success_rate = loop_success_count / T
    theoretical_rate = calculate_theoretical_success_rate(N)
    
    # 打印结果
    print(f"\n模拟结果汇总:")
    print(f"随机搜索策略成功率: {random_success_rate:.6f} ({random_success_count}/{T})")
    print(f"循环搜索策略成功率: {loop_success_rate:.6f} ({loop_success_count}/{T})")
    print(f"理论成功率: {theoretical_rate:.6f}")
    
    # 可视化循环策略的成功分布
    plt.figure(figsize=(10, 6))
    plt.bar(["随机策略", "循环策略", "理论值"], 
            [random_success_rate, loop_success_rate, theoretical_rate],
            color=['blue', 'green', 'orange'])
    plt.ylim(0, 1)
    plt.title(f'策略成功率对比 (N={N}, K={K})')
    plt.ylabel('成功率')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    
    return random_success_rate, loop_success_rate, theoretical_rate

if __name__ == "__main__":
    # 运行默认参数的模拟
    run_simulation()    