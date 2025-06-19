# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
#     "fire",
# ]
# ///


from typing import Any
from abc import ABC, abstractmethod
import random

import matplotlib.pyplot as plt
import numpy as np


def get_user_input() -> tuple[int, int, int]:
    """
    获取用户输入参数

    Returns:
        tuple[int, int, int]: (囚犯数量, 每人尝试次数, 模拟轮次)
    """
    try:
        n = int(input("请输入囚犯数量 N (默认100): ") or "100")
        k = int(input("请输入每人尝试次数 K (默认50): ") or "50")
        t = int(input("请输入模拟轮次 T (默认10000): ") or "10000")
        return n, k, t
    except ValueError:
        print("输入无效，使用默认值")
        return 100, 50, 10000


def output_results(results: dict[str, Any]) -> None:
    """
    输出模拟结果

    Args:
        results: 包含模拟结果的字典
    """
    print("\n" + "=" * 50)
    print("囚犯抽签问题模拟结果")
    print("=" * 50)
    print(f"参数设置:")
    print(f"  囚犯数量: {results['n']}")
    print(f"  每人尝试次数: {results['k']}")
    print(f"  模拟轮次: {results['trials']}")
    print()
    print(f"结果:")
    print(
        f"  策略1 (随机搜索) 成功率: {results['random_success_rate']:.4f} ({results['random_success_rate'] * 100:.2f}%)"
    )
    print(
        f"  策略2 (循环策略) 成功率: {results['loop_success_rate']:.4f} ({results['loop_success_rate'] * 100:.2f}%)"
    )
    print(
        f"\n  循环策略相对优势: {results['loop_success_rate'] / (results['random_success_rate'] + 1e-6):.2f}倍"
    )
    print(f"  理论计算的循环策略成功率: {results['theoretical_success_rate']:.4f}")
    print("=" * 50)


# region strategies


class Strategy(ABC):
    """策略抽象基类"""

    @abstractmethod
    def search(self, prisoner_id: int, boxes: list[int], max_attempts: int) -> bool:
        """
        搜索策略接口

        Args:
            prisoner_id: 囚犯编号 (1-based)
            boxes: 盒子数组，boxes[i]表示第i+1个盒子中的纸条编号
            max_attempts: 最大尝试次数

        Returns:
            bool: 是否找到自己的编号
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """策略名称"""
        pass


class RandomStrategy(Strategy):
    """随机搜索策略：囚犯随机打开盒子"""

    @property
    def name(self) -> str:
        return "随机搜索"

    def search(self, prisoner_id: int, boxes: list[int], max_attempts: int) -> bool:
        """
        随机搜索实现

        Args:
            prisoner_id: 囚犯编号 (1-based)
            boxes: 盒子数组，boxes[i]表示第i+1个盒子中的纸条编号
            max_attempts: 最大尝试次数

        Returns:
            bool: 是否找到自己的编号
        """
        available_boxes = list(range(len(boxes)))
        random.shuffle(available_boxes)

        for i in range(min(max_attempts, len(available_boxes))):
            box_index = available_boxes[i]
            if boxes[box_index] == prisoner_id:
                return True
        return False


class LoopStrategy(Strategy):
    """循环策略：囚犯从自己编号的盒子开始，跟随纸条编号形成的循环"""

    @property
    def name(self) -> str:
        return "循环策略"

    def search(self, prisoner_id: int, boxes: list[int], max_attempts: int) -> bool:
        """
        循环策略实现

        Args:
            prisoner_id: 囚犯编号 (1-based)
            boxes: 盒子数组，boxes[i]表示第i+1个盒子中的纸条编号
            max_attempts: 最大尝试次数

        Returns:
            bool: 是否找到自己的编号
        """
        current_box = prisoner_id - 1  # 转换为0-based索引

        for _ in range(max_attempts):
            paper_number = boxes[current_box]
            if paper_number == prisoner_id:
                return True
            current_box = paper_number - 1  # 转换为0-based索引

        return False


# endregion strategies


def create_random_boxes(n: int) -> list[int]:
    """
    创建随机排列的盒子（确保无重复）

    Args:
        n: 盒子/囚犯数量

    Returns:
        list[int]: 随机排列的纸条编号列表
    """
    papers = list(range(1, n + 1))
    random.shuffle(papers)
    return papers


def simulate_single_round(n: int, k: int, strategy: Strategy) -> bool:
    """
    模拟单轮游戏

    Args:
        n: 囚犯数量
        k: 每人最大尝试次数
        strategy: 策略实例

    Returns:
        bool: 所有囚犯是否都成功找到自己的编号
    """
    boxes = create_random_boxes(n)

    for prisoner_id in range(1, n + 1):
        if not strategy.search(prisoner_id, boxes, k):
            return False
    return True


def run_simulation(n: int, k: int, trials: int) -> tuple[float, float]:
    """
    运行完整模拟

    Args:
        n: 囚犯数量
        k: 每人最大尝试次数
        trials: 模拟轮次

    Returns:
        tuple[float, float]: (随机策略成功率, 循环策略成功率)
    """
    random_strategy = RandomStrategy()
    loop_strategy = LoopStrategy()

    random_successes = 0
    loop_successes = 0

    for _ in range(trials):
        if simulate_single_round(n, k, random_strategy):
            random_successes += 1
        if simulate_single_round(n, k, loop_strategy):
            loop_successes += 1

    return random_successes / trials, loop_successes / trials


def calculate_theoretical_success_rate(n: int, k: int) -> float:
    """
    计算循环策略的理论成功率

    基于排列循环理论：成功的条件是所有循环长度都不超过k

    Args:
        n: 囚犯数量
        k: 每人最大尝试次数

    Returns:
        float: 理论成功率
    """
    # 使用调和级数近似计算
    # P(成功) ≈ 1 - ln(n/k)，当k=n/2时
    if k >= n:
        return 1.0
    elif k == n // 2:
        # 精确计算：P = 1 - H(n) + H(k)，其中H(i)是第i个调和数
        harmonic_n = sum(1 / i for i in range(k + 1, n + 1))
        return 1 - harmonic_n
    else:
        # 一般情况的近似
        return max(0, 1 - np.log(n / k))


def plot_results(results: dict[str, Any]):
    """
    绘制结果图表

    Args:
        results: 包含模拟结果的字典
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 左图：成功率对比
    strategies = ["Random", "Loop", "Optimal"]
    success_rates = [
        results["random_success_rate"],
        results["loop_success_rate"],
        results["theoretical_success_rate"],
    ]
    colors = ["red", "blue", "green"]

    bars = ax1.bar(strategies, success_rates, color=colors, alpha=0.7)
    ax1.set_ylabel("Success Rate")
    ax1.set_title("Strategy Comparison")
    ax1.set_ylim(0, max(success_rates) * 1.1)

    # 在柱状图上显示数值
    for bar, rate in zip(bars, success_rates):
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + height * 0.01,
            f"{rate:.4f}",
            ha="center",
            va="bottom",
        )

    # 右图：参数敏感性分析
    k_values = range(10, results["n"], 5)
    theoretical_rates = [
        calculate_theoretical_success_rate(results["n"], k) for k in k_values
    ]

    ax2.plot(k_values, theoretical_rates, "g-", linewidth=2, label="Theoretical")
    ax2.axvline(
        x=results["k"],
        color="red",
        linestyle="--",
        alpha=0.7,
        label=f"When k={results['k']}",
    )
    ax2.axhline(
        y=results["loop_success_rate"],
        color="blue",
        linestyle="--",
        alpha=0.7,
        label="Simulated",
    )

    ax2.set_xlabel("Tries/person (k)")
    ax2.set_ylabel("Success Rate")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("result.png")
    plt.show()


def plot_parameter_analysis(n: int, max_trials: int = 5000) -> None:
    """
    绘制参数分析图

    Args:
        n: 囚犯数量
        max_trials: 最大模拟轮次
    """

    # 分析不同k值对成功率的影响
    k_values = range(1, n, max(1, n // 20))
    random_rates = []
    loop_rates = []
    theoretical_rates = []

    # 创建策略实例
    random_strategy = RandomStrategy()
    loop_strategy = LoopStrategy()

    print("正在进行参数敏感性分析...")
    for i, k in enumerate(k_values):
        trials = min(max_trials, max(100, 1000 // max(1, k // 10)))

        # 运行模拟
        random_successes = 0
        loop_successes = 0

        for _ in range(trials):
            if simulate_single_round(n, k, random_strategy):
                random_successes += 1
            if simulate_single_round(n, k, loop_strategy):
                loop_successes += 1

        random_rate = random_successes / trials
        loop_rate = loop_successes / trials
        theoretical_rate = calculate_theoretical_success_rate(n, k)

        random_rates.append(random_rate)
        loop_rates.append(loop_rate)
        theoretical_rates.append(theoretical_rate)

    # 绘制结果
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, random_rates, "r-", label="Random", alpha=0.7)
    plt.plot(k_values, loop_rates, "b-", label="Loop", linewidth=2)
    plt.plot(k_values, theoretical_rates, "g--", label="Sim Optimal", linewidth=2)

    plt.xlabel("Tries/person (k)")
    plt.ylabel("Success Rate")
    plt.title(f"Strategies Comparison (n={n})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(1, n - 1)
    plt.ylim(0, 1)

    # 标记关键点
    plt.axvline(
        x=n // 2, color="orange", linestyle=":", alpha=0.7, label=f"k=n/2={n // 2}"
    )
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"analyze{n}.png")
    plt.show()


def main() -> None:
    n, k, trials = get_user_input()

    print(f"\n开始模拟 (n={n}, k={k}, trials={trials})...")

    random_success_rate, loop_success_rate = run_simulation(n, k, trials)

    theoretical_success_rate = calculate_theoretical_success_rate(n, k)

    results = {
        "n": n,
        "k": k,
        "trials": trials,
        "random_success_rate": random_success_rate,
        "loop_success_rate": loop_success_rate,
        "theoretical_success_rate": theoretical_success_rate,
    }

    output_results(results)

    show_plot = input("\n是否显示结果图表? (y/n, 默认y): ").lower()
    if show_plot != "n":
        plot_results(results)


if __name__ == "__main__":
    try:
        import fire

        fire.Fire(
            {
                "solve": main,
                "analyze": plot_parameter_analysis,
            }
        )
    except ImportError:
        print("使用[pip install fire]来获得全功能使用")
        main()
