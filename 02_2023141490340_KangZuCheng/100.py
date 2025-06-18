import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb


def generate_boxes(n):
    """生成随机排列的盒子"""
    numbers = list(range(1, n + 1))
    random.shuffle(numbers)
    return numbers


def strategy_random(boxes, prisoner_id, k):
    """随机搜索策略"""
    n = len(boxes)
    boxes_to_open = random.sample(range(n), k)
    for box_idx in boxes_to_open:
        if boxes[box_idx] == prisoner_id:
            return True
    return False


def strategy_cycle(boxes, prisoner_id, k):
    """循环搜索策略"""
    current_box = prisoner_id - 1  # 盒子索引从0开始
    for _ in range(k):
        if boxes[current_box] == prisoner_id:
            return True
        current_box = boxes[current_box] - 1
    return False


def run_simulation(n, k, t, strategy_func):
    """运行指定策略的模拟"""
    successes = 0
    for _ in range(t):
        boxes = generate_boxes(n)
        all_success = True
        for prisoner_id in range(1, n + 1):
            if not strategy_func(boxes, prisoner_id, k):
                all_success = False
                break
        if all_success:
            successes += 1
    success_rate = successes / t
    return success_rate, successes


def calculate_theoretical_success_rate(n, k):
    """计算理论成功率"""
    if k < n / 2:
        return 0.0
    sum_prob = 0.0
    for m in range(k + 1, n + 1):
        sum_prob += 1 / m
    return 1.0 - sum_prob


def main():
    # 默认参数
    n = 100  # 囚犯数量
    k = 50  # 尝试次数
    t = 10000  # 模拟轮次

    # 策略1：随机搜索
    success_rate_random, successes_random = run_simulation(n, k, t, strategy_random)
    print(f"随机搜索策略:")
    print(f"总轮次: {t}, 成功轮次: {successes_random}, 成功率: {success_rate_random:.6f}")

    # 策略2：循环策略
    success_rate_cycle, successes_cycle = run_simulation(n, k, t, strategy_cycle)
    print(f"\n循环搜索策略:")
    print(f"总轮次: {t}, 成功轮次: {successes_cycle}, 成功率: {success_rate_cycle:.6f}")

    # 理论成功率
    theoretical_rate = calculate_theoretical_success_rate(n, k)
    print(f"\n理论计算成功率: {theoretical_rate:.6f}")

    # 扩展分析：不同N和K值
    print("\n扩展分析：不同N和K值的成功率")
    test_params = [(50, 25), (80, 40), (120, 60)]
    for test_n, test_k in test_params:
        rate_cycle, _ = run_simulation(test_n, test_k, t, strategy_cycle)
        rate_random, _ = run_simulation(test_n, test_k, t, strategy_random)
        theo_rate = calculate_theoretical_success_rate(test_n, test_k)
        print(
            f"N={test_n}, K={test_k}: 随机策略成功率={rate_random:.6f}, 循环策略成功率={rate_cycle:.6f}, 理论成功率={theo_rate:.6f}")

    # 绘制成功率分布直方图
    plt.figure(figsize=(10, 6))
    strategies = ['随机搜索', '循环搜索']
    success_rates = [success_rate_random, success_rate_cycle]
    plt.bar(strategies, success_rates, color=['skyblue', 'lightgreen'])
    plt.ylim(0, 1.0)
    plt.title(f'两种策略的成功率对比 (N={n}, K={k}, T={t})')
    plt.ylabel('成功率')

    # 添加数值标签
    for i, v in enumerate(success_rates):
        plt.text(i, v + 0.01, f'{v:.6f}', ha='center')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()