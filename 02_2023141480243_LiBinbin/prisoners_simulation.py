import random
import os


def random_search_strategy(N, K):
    """随机搜索策略，返回该轮成功人数"""
    boxes = list(range(1, N + 1))  # 生成 1 到 N 的盒子编号
    total_success = 0  # 记录成功人数

    # 对每个囚犯进行 K 次随机尝试
    for prisoner_id in range(1, N + 1):
        prisoner_boxes = random.sample(boxes, K)  # 随机选择 K 个盒子
        if prisoner_id in prisoner_boxes:
            total_success += 1  # 该囚犯成功

    return total_success  # 返回该轮成功人数


def cyclic_search_strategy(N, K):
    """循环策略，返回该轮成功人数"""
    boxes = list(range(1, N + 1))
    random.shuffle(boxes)  # 随机打乱盒子中的编号
    total_success = 0  # 记录成功人数

    for prisoner in range(1, N + 1):
        current_box = prisoner

        for _ in range(K):
            if boxes[current_box - 1] == prisoner:
                total_success += 1  # 该囚犯成功
                break  # 找到之后结束查找
            current_box = boxes[current_box - 1]  # 跳转到盒子中的编号

    return total_success  # 返回该轮成功人数


# 获取用户输入
def get_user_input():
    N = 100  # 默认囚犯数量
    K = 50  # 默认每人尝试次数
    T = None

    user_input = input("请输入囚犯数量 N（默认100），每人尝试次数 K（默认50），或仅输入模拟轮次 T（如10000）：").strip()

    if user_input.isdigit():
        T = int(user_input)  # 只有T被直接输入
    else:
        parts = user_input.split()
        if len(parts) == 1:
            T = int(parts[0])  # 只有 T
        elif len(parts) == 2:
            N = int(parts[0])  # 只有 N 和 K
            K = int(parts[1])
            T = int(input("请输入模拟轮次 T（如10000）：").strip())  # 提示输入 T
        elif len(parts) == 3:
            N = int(parts[0])  # 所有参数
            K = int(parts[1])
            T = int(parts[2])

    return N, K, T


# 获取输入参数
N, K, T = get_user_input()

# 初始化成功计数
random_success_count = 0
cyclic_success_count = 0

# 运行实验并逐轮输出
for round_number in range(1, T + 1):
    # 设置随机种子
    random.seed(int.from_bytes(os.urandom(4), 'little'))  # 使用系统随机数作为种子

    random_success = random_search_strategy(N, K)
    cyclic_success = cyclic_search_strategy(N, K)

    # 输出当前轮次结果
    print(f"round:{round_number} "
          f"strategy1:{'succeed' if random_success > 0 else 'fail'} ({random_success}/{N}) "
          f"strategy2:{'succeed' if cyclic_success > 0 else 'fail'} ({cyclic_success}/{N})")

    # 更新成功计数
    if random_success == N:  # 如果所有囚犯都成功
        random_success_count += 1
    if cyclic_success == N:  # 如果所有囚犯都成功
        cyclic_success_count += 1

# 计算最终成功率
random_success_rate = random_success_count / T
cyclic_success_rate = cyclic_success_count / T

# 输出最终成功概率
print(f"随机搜索成功率: {random_success_rate:.2f}")
print(f"循环策略成功率: {cyclic_success_rate:.2f}")