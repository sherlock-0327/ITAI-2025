import random


def simulate_random_strategy(N, K, T):
    """模拟随机策略"""
    success_count = 0

    for _ in range(T):
        # 创建盒子配置
        boxes = list(range(1, N + 1))
        random.shuffle(boxes)

        all_success = True

        for prisoner in range(1, N + 1):
            found = False
            attempts = set()

            for _ in range(K):
                # 随机选择一个未尝试过的盒子
                box = random.randint(0, N - 1)
                while box in attempts:
                    box = random.randint(0, N - 1)
                attempts.add(box)

                if boxes[box] == prisoner:
                    found = True
                    break

            if not found:
                all_success = False
                break

        if all_success:
            success_count += 1

    success_rate = success_count / T * 100
    return success_rate


def simulate_cycle_strategy(N, K, T):
    """模拟循环策略"""
    success_count = 0

    for _ in range(T):
        # 创建盒子配置
        boxes = list(range(1, N + 1))
        random.shuffle(boxes)

        all_success = True

        for prisoner in range(1, N + 1):
            current_box = prisoner - 1  # 转换为0-based索引
            attempts = 0
            found = False

            while attempts < K:
                if boxes[current_box] == prisoner:
                    found = True
                    break
                # 跳转到盒子中的编号对应的盒子
                current_box = boxes[current_box] - 1
                attempts += 1

            if not found:
                all_success = False
                break

        if all_success:
            success_count += 1

    success_rate = success_count / T * 100
    return success_rate


def main():
    # 默认参数
    N = 100
    K = 50
    T = 10000

    # 获取用户输入
    try:
        input_N = input(f"输入囚犯数量N (默认{N}): ")
        if input_N:
            N = int(input_N)

        input_K = input(f"输入每人尝试次数K (默认{K}): ")
        if input_K:
            K = int(input_K)

        input_T = input(f"输入模拟轮次T (默认{T}): ")
        if input_T:
            T = int(input_T)
    except ValueError:
        print("无效输入，将使用默认值")

    # 模拟两种策略
    print(f"\n开始模拟，参数: N={N}, K={K}, T={T}")

    print("\n模拟随机策略...")
    random_success_rate = simulate_random_strategy(N, K, T)
    print(f"随机策略成功率: {random_success_rate:.4f}%")

    print("\n模拟循环策略...")
    cycle_success_rate = simulate_cycle_strategy(N, K, T)
    print(f"循环策略成功率: {cycle_success_rate:.4f}%")

    print("\n结果对比:")
    print(f"循环策略比随机策略成功率高 {cycle_success_rate - random_success_rate:.2f}%")


if __name__ == "__main__":
    main()