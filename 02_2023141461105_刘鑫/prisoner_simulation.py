# -*- coding: utf-8 -*-
import random
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题


def simulate_random_strategy(N, K, T):
    """
    策略1：随机搜索
    每个囚犯随机打开K个盒子，判断是否找到自己编号
    返回成功次数和每轮成功/失败列表
    """
    success_count = 0
    results = []
    for _ in range(T):
        boxes = list(range(N))
        random.shuffle(boxes)
        all_found = True
        for prisoner in range(N):
            opened = random.sample(range(N), K)
            if prisoner not in [boxes[i] for i in opened]:
                all_found = False
                break
        results.append(1 if all_found else 0)
        if all_found:
            success_count += 1
    return success_count, results

def simulate_loop_strategy(N, K, T):
    """
    策略2：循环策略
    每个囚犯从自己编号对应盒子开始，按盒子内编号跳转，最多尝试K次
    返回成功次数和每轮成功/失败列表
    """
    success_count = 0
    results = []
    for _ in range(T):
        boxes = list(range(N))
        random.shuffle(boxes)
        all_found = True
        for prisoner in range(N):
            next_box = prisoner
            for _ in range(K):
                if boxes[next_box] == prisoner:
                    break
                next_box = boxes[next_box]
            else:  # 未在K次尝试内找到
                all_found = False
                break
        results.append(1 if all_found else 0)
        if all_found:
            success_count += 1
    return success_count, results

def plot_results(loop_results, T):
    """
    画出循环策略的累计成功率曲线和成功/失败次数柱状图
    """
    cumulative_success = np.cumsum(loop_results) / np.arange(1, T + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(cumulative_success, label="循环策略累计成功率")
    plt.xlabel("模拟轮次")
    plt.ylabel("累计成功率")
    plt.title("循环策略累计成功率随模拟轮次变化")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("runtime_cumulative_success.png")
    plt.show()

    successes = sum(loop_results)
    failures = T - successes
    plt.figure(figsize=(6, 6))
    plt.bar(['成功', '失败'], [successes, failures], color=['green', 'red'])
    plt.title("循环策略成功/失败次数统计")
    plt.ylabel("次数")
    plt.tight_layout()
    plt.savefig("runtime_success_failure_bar.png")
    plt.show()

def main():
    # 参数输入，默认值
    try:
        N = int(input("请输入囚犯数量N（默认100）：") or 100)
        K = int(input("请输入每人最大尝试次数K（默认50）：") or 50)
        T = int(input("请输入模拟轮次T（默认10000）：") or 10000)
        if N < 1 or K < 1 or T < 1:
            print("参数必须为正整数，使用默认值。")
            N, K, T = 100, 50, 10000
    except:
        print("输入错误，使用默认值。")
        N, K, T = 100, 50, 10000

    print(f"开始模拟：囚犯数={N}, 最大尝试次数={K}, 模拟轮次={T}")
    print("策略1（随机搜索）模拟中，请稍候...")
    rand_success, _ = simulate_random_strategy(N, K, T)
    print("策略2（循环策略）模拟中，请稍候...")
    loop_success, loop_results = simulate_loop_strategy(N, K, T)

    print(f"策略1（随机搜索）成功率：{rand_success / T:.4f}")
    print(f"策略2（循环策略）成功率：{loop_success / T:.4f}")

    plot_results(loop_results, T)

if __name__ == "__main__":
    main()