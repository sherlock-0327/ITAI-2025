# ranluyao 2025/6/10 at SCU

import random
def box_init(num: int)-> list:
    '''
    Initialize the boxes
    :param num: the number of prisoners
    :return: boxes:list
    '''
    boxes = list(range(num))
    random.shuffle(boxes)
    return boxes

def random_strategy(num_prisoners: int , boxes: list, tries: int, epoches: int) -> float:
    '''
    this is a random strategy for this quesiton
    :param num_prisoners: the number of prisoners
    :param boxes: the boxes list which prisoners will choose
    :param tries: total tries for each prisoner
    :param epoches: total epoches for all prisoners
    :return: success rate:float
    '''
    successes = 0
    for _ in range(epoches):
        all_found = True
        for prisoner in range(num_prisoners):
            found = False
            chosen_box = random.sample(range(num_prisoners), tries)
            for index in chosen_box:
                if boxes[index] == prisoner:
                    found = True
                    break
            if not found:
                all_found = False
                break
        if all_found:
            successes += 1
    return successes / epoches

def cycle_strategy(num_prisoners: int, boxes: list, tries: int, epoches: int) -> float:
    '''
    this is a cycle strategy for this quesiton
    :param num_prisoners: the number of prisoners
    :param boxes: the boxes list which prisoners will choose
    :param tries: total tries for each prisoner
    :param epoches: total epoches for all prisoners
    :return: success rate:float
    '''
    successes = 0
    for _ in range(epoches):
        all_found = True
        for prisoner in range(num_prisoners):
            found = False
            box_index = prisoner
            for _ in range(tries):
                if boxes[box_index] == prisoner:
                    found = True
                    break
                box_index = boxes[box_index]
            if not found:
                all_found = False
                break
        if all_found:
            successes += 1
    return successes / epoches

if __name__ == '__main__':

    N = input("input the number of prisoners")
    K = input("input the total tries for each prisoner")
    T = input("input the total epoches for all prisoners")
    N = int(N)
    K = int(K)
    T = int(T)

    boxes = box_init(N)
    random_rate = random_strategy(N, boxes, K, T)
    cycle_rate = cycle_strategy(N, boxes, K, T)

    print(f"正在模拟 {N} 名囚犯，每人尝试 {K} 次，共进行 {T} 轮实验...")
    print(f"随机策略的成功率为 {random_rate:.6f}")
    print(f"循环策略的成功率为 {cycle_rate:.6f}")