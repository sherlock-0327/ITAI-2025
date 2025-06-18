import random
from typing import List

def generate_random_boxes(n: int) -> List[int]:
    """生成随机排列的盒子内容"""
    numbers = list(range(1, n+1))
    random.shuffle(numbers)
    return numbers

def strategy_random(boxes: List[int], prisoner_num: int, max_attempts: int) -> bool:
    """随机策略：随机选择盒子"""
    attempts = random.sample(range(len(boxes)), max_attempts)
    for attempt in attempts:
        if boxes[attempt] == prisoner_num:
            return True
    return False

def strategy_cycle(boxes: List[int], prisoner_num: int, max_attempts: int) -> bool:
    """循环策略：跟随盒子中的数字跳转"""
    current_box = prisoner_num - 1  # 转换为0-based索引
    for _ in range(max_attempts):
        if boxes[current_box] == prisoner_num:
            return True
        current_box = boxes[current_box] - 1  # 跳转到下一个盒子
    return False

def run_simulation(n: int, k: int, strategy) -> bool:
    """运行一次模拟"""
    boxes = generate_random_boxes(n)
    for prisoner_num in range(1, n+1):
        if not strategy(boxes, prisoner_num, k):
            return False
    return True

def compare_strategies(n: int = 50, k: int = 25, t: int = 10000):
    """比较两种策略的成功率"""
    random_success = 0
    cycle_success = 0
    
    for _ in range(t):
        # 对两种策略使用相同的盒子排列
        boxes = generate_random_boxes(n)
        
        # 测试随机策略
        random_failed = False
        for prisoner_num in range(1, n+1):
            if not strategy_random(boxes, prisoner_num, k):
                random_failed = True
                break
        if not random_failed:
            random_success += 1
        
        # 测试循环策略
        cycle_failed = False
        for prisoner_num in range(1, n+1):
            if not strategy_cycle(boxes, prisoner_num, k):
                cycle_failed = True
                break
        if not cycle_failed:
            cycle_success += 1
    
    print(f"set: {n} prisoners, {k} tries per person, {t} simulation")
    print(f"random strategy succeed probability: {random_success/t:.6f} ({random_success}/{t})")
    print(f"c: {cycle_success/t:.6f} ({cycle_success}/{t})")

if __name__ == "__main__":
    # 默认参数: N=100, K=50, T=10000
    compare_strategies(n=50, k=25, t=10000)