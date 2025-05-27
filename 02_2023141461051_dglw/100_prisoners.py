import numpy as np
import matplotlib.pyplot as plt

#此处注释全部是未进行大规模T优化前的版本，在这里使用的是优化后的版本（因为速度快一点）
""""
# 随机搜索策略函数
def random_search_strategy(prisoners, boxes, attempts):
    success_count = 0
    for prisoner in prisoners:
        tried_boxes = set()
        for _ in range(attempts):
            box = random.choice(boxes) #随机生成
            if box not in tried_boxes:
                tried_boxes.add(box)
                if box == prisoner:
                    success_count += 1 #成功人数加1
                    break
    return success_count == len(prisoners) #代表成功人数


# 循环搜索策略函数
def cycle_search_strategy(prisoners, boxes, attempts):
    success_count = 0
    for prisoner in prisoners:
        current_box = prisoner
        tried_count = 0
        while tried_count < attempts:
            if boxes[current_box - 1] == prisoner:
                success_count += 1 #成功人数加1
                break
            current_box = boxes[current_box - 1]
            tried_count += 1
    return success_count == len(prisoners) #代表成功人数


# 模拟函数
def simulate(prisoner_num=100, attempt_num=50, round_num=10000):
    prisoners = list(range(1, prisoner_num + 1))
    random_success_rate_list = []
    cycle_success_rate_list = []
    random_per_round_result = []  # 新增列表用于存储随机策略每轮结果
    cycle_per_round_result = []  # 新增列表用于存储循环策略每轮结果
    for _ in range(round_num):
        boxes = prisoners.copy()
        random.shuffle(boxes)
        random_success = random_search_strategy(prisoners, boxes, attempt_num)
        cycle_success = cycle_search_strategy(prisoners, boxes, attempt_num)
        random_success_rate_list.append(random_success)
        cycle_success_rate_list.append(cycle_success)
        random_per_round_result.append("成功" if random_success else "失败")  # 记录随机策略本轮结果
        cycle_per_round_result.append("成功" if cycle_success else "失败")  # 记录循环策略本轮结果
    #计算两种策略的成功率
    random_success_rate = sum(random_success_rate_list) / round_num
    cycle_success_rate = sum(cycle_success_rate_list) / round_num
    return random_success_rate, cycle_success_rate, random_per_round_result, cycle_per_round_result
"""

# 随机搜索策略函数（向量优化版本）
def random_search_strategy(prisoners, boxes, attempts):
    """
     prisoners: 包含所有囚犯编号的一维数组。
     boxes: 包含盒子内纸条编号的一维数组，表示囚犯编号的一种随机排列。
     attempts: 每个囚犯可尝试打开盒子的次数。
     return: 如果所有囚犯都在规定尝试次数内找到自己的编号，返回True；否则返回False。
    """
    n_prisoners = len(prisoners)
    # 一次性生成所有囚犯在所有尝试中的随机选择，
    # 其中每个元素表示对应囚犯在对应尝试中选择的盒子编号
    random_choices = np.random.choice(n_prisoners, size=(n_prisoners, attempts))
    # 设置一个与囚犯数量等长的布尔数组，用于记录每个囚犯是否找到自己的编号，初始值为False
    found = np.zeros(n_prisoners, dtype=bool)
    for i in range(attempts):
        # 获取当前尝试中所有囚犯选择的盒子编号
        current_choices = random_choices[:, i]
        # 使用逻辑或操作更新found数组，判断当前尝试中哪些囚犯找到了自己的编号
        found |= (boxes[current_choices] == prisoners)
        if np.all(found):
            # 如果所有囚犯都已找到自己的编号，提前返回True
            return True
    # 所有尝试结束后，判断是否所有囚犯都找到了自己的编号
    return np.all(found)


# 循环搜索策略函数（向量优化版本）
def cycle_search_strategy(prisoners, boxes, attempts):
    """
     prisoners: 包含所有囚犯编号的一维数组，元素类型为整数。
     boxes: 包含盒子内纸条编号的一维数组，元素类型为整数，是囚犯编号的一种随机排列。
     attempts: 每个囚犯可尝试打开盒子的次数，为整数。
     return: 如果所有囚犯都在规定尝试次数内找到自己的编号，返回True；否则返回False。
    """
    n_prisoners = len(prisoners)
    # 复制囚犯编号数组，用于记录每个囚犯当前所在的盒子编号，初始为自己的编号
    current_boxes = prisoners.copy()
    # 设置一个与囚犯数量等长的布尔数组，用于记录每个囚犯是否找到自己的编号，初始值为False
    found = np.zeros(n_prisoners, dtype=bool)
    for _ in range(attempts):
        # 使用逻辑或操作更新found数组，判断当前尝试中哪些囚犯找到了自己的编号
        found |= (boxes[current_boxes - 1] == prisoners)
        if np.all(found):
            # 如果所有囚犯都已找到自己的编号，提前返回True
            return True
        # 更新每个囚犯下一次要打开的盒子编号
        current_boxes = boxes[current_boxes - 1]
    # 所有尝试结束后，判断是否所有囚犯都找到了自己的编号
    return np.all(found)


# 模拟函数（向量优化版本）
def simulate(prisoner_num=100, attempt_num=50, round=10000):
    """
    prisoner_num: 囚犯的数量，默认为100。
    attempt_num: 每个囚犯可尝试打开盒子的次数，默认为50。
    round: 模拟的轮次数量，默认为10000。
    return: 一个包含四个元素的元组，分别为随机搜索策略的成功率、循环搜索策略的成功率、
             随机搜索策略每轮的结果列表（元素为"成功"或"失败"字符串）。
             循环搜索策略每轮的结果列表（元素为"成功"或"失败"字符串）。
    """
    # 生成包含所有囚犯编号的一维数组
    prisoners = np.arange(1, prisoner_num + 1)
    random_success_rate_list = []
    cycle_success_rate_list = []
    random_per_round_result = []
    cycle_per_round_result = []

    # 一次性生成所有轮次的盒子编号排列，
    # 其中每一行表示一轮模拟中盒子内纸条编号的排列
    all_boxes = np.array([np.random.permutation(prisoners) for _ in range(round)])

    for i in range(round):
        # 获取当前轮次的盒子编号排列
        boxes = all_boxes[i]
        # 执行随机搜索策略并记录结果
        random_success = random_search_strategy(prisoners, boxes, attempt_num)
        # 执行循环搜索策略并记录结果
        cycle_success = cycle_search_strategy(prisoners, boxes, attempt_num)
        random_success_rate_list.append(random_success)
        cycle_success_rate_list.append(cycle_success)
        random_per_round_result.append("成功" if random_success else "失败")
        cycle_per_round_result.append("成功" if cycle_success else "失败")

    # 计算随机搜索策略的成功率
    random_success_rate = np.mean(random_success_rate_list)
    # 计算循环搜索策略的成功率
    cycle_success_rate = np.mean(cycle_success_rate_list)
    return random_success_rate, cycle_success_rate, random_per_round_result, cycle_per_round_result

# 主函数
def main():
    prisoner_num = int(input("请输入囚犯数量 N（默认 100）: ") or 100)
    attempt_num = int(input("请输入每人尝试次数 K（默认 50）: ") or 50)
    round_num = int(input("请输入模拟轮次 T（默认 10000）: ") or 10000)

    random_rate, cycle_rate, random_per_round, cycle_per_round = simulate(prisoner_num, attempt_num, round_num)
    print("随机搜索策略每轮结果:")
    for i, result in enumerate(random_per_round):
        print(f"第{i + 1}轮: {result}")
    print(f"随机搜索策略总成功率: {random_rate}")

    print("循环搜索策略每轮结果:")
    for i, result in enumerate(cycle_per_round):
        print(f"第{i + 1}轮: {result}")
    print(f"循环搜索策略总成功率: {cycle_rate}")

    # 扩展分析：调整N和K的值 这里根据题目要求进行设置N=50 K=25 round不变
    new_prisoner_num = 50
    new_attempt_num = 25
    new_random_rate, new_cycle_rate, new_random_per_round, new_cycle_per_round = simulate(new_prisoner_num, new_attempt_num, round_num)
    print(f"调整后随机搜索策略成功率（N={new_prisoner_num}, K={new_attempt_num}）: {new_random_rate}")
    print(f"调整后循环搜索策略成功率（N={new_prisoner_num}, K={new_attempt_num}）: {new_cycle_rate}")

    # 绘制循环策略成功人数分布图（使用向量化函数）
    prisoners = np.arange(1, 101)  # N=100
    attempt_num = 50  # K=50
    round_num = 10000  # ROUND=10000

    # 生成所有轮次的盒子排列
    all_boxes = np.array([np.random.permutation(prisoners) for _ in range(round_num)])

    # 向量化计算每轮成功人数
    cycle_success_counts = np.array([
        cycle_search_strategy_count(prisoners, boxes, attempt_num)
        for boxes in all_boxes
    ])

    # 绘制概率密度直方图
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(
        cycle_success_counts,
        bins=50,
        density=True,
        alpha=0.7,
        color='skyblue',
        label='result'
    )


    # 添加全员成功概率标记
    all_success_prob = np.sum(cycle_success_counts == 100) / round_num
    plt.axvline(
        x=100,
        color='green',
        linestyle='--',
        linewidth=2,
        label=f'The probability of success for all: {all_success_prob:.4f}'
    )

    # 图表基本信息
    plt.xlabel('success_prisoners', fontsize=12) #成功人数
    plt.ylabel('Probability density', fontsize=12) #概率密度
    plt.title(f'The distribution of successful people in the circular strategy(N=100, K=50, T={round_num})', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


# 循环搜索策略函数（向量优化版本，返回成功人数）用于画图
def cycle_search_strategy_count(prisoners, boxes, attempts):
    n_prisoners = len(prisoners)
    current_boxes = prisoners.copy()
    found = np.zeros(n_prisoners, dtype=bool)

    for _ in range(attempts):
        found |= (boxes[current_boxes - 1] == prisoners)
        current_boxes = boxes[current_boxes - 1]

    return np.sum(found)  # 返回成功人数


if __name__ == "__main__":
    main()