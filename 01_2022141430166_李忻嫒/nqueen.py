# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "fire",
#   "matplotlib",
# ]
# ///


import time
from abc import ABC, abstractmethod

# region strategies


class HeuristicStrategy(ABC):
    """启发式搜索策略接口"""

    @abstractmethod
    def select_next_position(
        self,
        n: int,
        row: int,
        occupied_cols: set,
        occupied_diag1: set,
        occupied_diag2: set,
    ) -> list[int]:
        """
        选择下一个位置的策略
        返回按优先级排序的列位置列表
        """
        pass


class BasicStrategy(HeuristicStrategy):
    """基础策略：按列顺序尝试"""

    def select_next_position(
        self,
        n: int,
        row: int,
        occupied_cols: set,
        occupied_diag1: set,
        occupied_diag2: set,
    ) -> list[int]:
        return [col for col in range(n) if col not in occupied_cols]


class MinConflictStrategy(HeuristicStrategy):
    """最小冲突策略：优先选择冲突最少的位置"""

    def select_next_position(
        self,
        n: int,
        row: int,
        occupied_cols: set,
        occupied_diag1: set,
        occupied_diag2: set,
    ) -> list[int]:
        available_cols = [col for col in range(n) if col not in occupied_cols]

        # 计算每个可用位置的冲突数
        conflict_counts = []
        for col in available_cols:
            conflicts = 0
            # 检查对角线冲突
            if (row - col) in occupied_diag1:
                conflicts += 1
            if (row + col) in occupied_diag2:
                conflicts += 1
            conflict_counts.append((conflicts, col))

        # 按冲突数排序，冲突少的优先
        conflict_counts.sort()
        return [col for _, col in conflict_counts]


# endregion strategies


class NQueensSolver:
    def __init__(self, heuristic_strategy: HeuristicStrategy = BasicStrategy()):
        self.heuristic_strategy = heuristic_strategy
        self.solutions_count = 0
        self.backtrack_count = 0
        self.pruning_count = 0
        self.last_solved_time = -1

    def solve_n_queens(self, n: int) -> list[list[int]]:
        """
        求解N皇后问题
        Args:
            n: 棋盘大小
        Returns:
            所有解的列表，每个解是一个列表，表示每行皇后的列位置
        """
        start_time = time.time()

        if n <= 0:
            return []

        self.solutions_count = 0
        self.backtrack_count = 0
        self.pruning_count = 0

        solutions = []
        board = [-1] * n  # board[i] 表示第i行皇后的列位置

        # 使用集合进行剪枝优化
        occupied_cols = set()  # 已占用的列
        occupied_diag1 = set()  # 已占用的主对角线 (row - col)
        occupied_diag2 = set()  # 已占用的副对角线 (row + col)

        self._backtrack(
            n, 0, board, solutions, occupied_cols, occupied_diag1, occupied_diag2
        )

        self.last_solved_time = time.time() - start_time

        return solutions

    def _backtrack(
        self,
        n: int,
        row: int,
        board: list[int],
        solutions: list[list[int]],
        occupied_cols: set,
        occupied_diag1: set,
        occupied_diag2: set,
    ):
        """
        回溯法求解
        """
        if row == n:
            # 找到一个解
            solutions.append(board[:])
            self.solutions_count += 1
            return

        # 使用启发式策略选择下一个位置
        candidate_cols = self.heuristic_strategy.select_next_position(
            n, row, occupied_cols, occupied_diag1, occupied_diag2
        )

        for col in candidate_cols:
            # 剪枝：检查是否与已放置的皇后冲突
            if self._is_valid_position(
                row, col, occupied_cols, occupied_diag1, occupied_diag2
            ):
                # 放置皇后
                board[row] = col
                occupied_cols.add(col)
                occupied_diag1.add(row - col)
                occupied_diag2.add(row + col)

                # 递归求解下一行
                self._backtrack(
                    n,
                    row + 1,
                    board,
                    solutions,
                    occupied_cols,
                    occupied_diag1,
                    occupied_diag2,
                )

                # 回溯：移除皇后
                occupied_cols.remove(col)
                occupied_diag1.remove(row - col)
                occupied_diag2.remove(row + col)
                self.backtrack_count += 1
            else:
                self.pruning_count += 1

    def _is_valid_position(
        self,
        row: int,
        col: int,
        occupied_cols: set,
        occupied_diag1: set,
        occupied_diag2: set,
    ) -> bool:
        """
        检查位置是否有效（剪枝优化）
        """
        return (
            col not in occupied_cols
            and (row - col) not in occupied_diag1
            and (row + col) not in occupied_diag2
        )

    def get_statistics(self) -> dict:
        return {
            "solutions_count": self.solutions_count,
            "backtrack_count": self.backtrack_count,
            "pruning_count": self.pruning_count,
        }


def print_board(solution: list[int]) -> None:
    """
    打印棋盘
    Args:
        solution: 解，表示每行皇后的列位置
    """
    n = len(solution)
    print("\n" + "=" * (4 * n + 1))
    for row in range(n):
        print("|", end="")
        for col in range(n):
            if solution[row] == col:
                print(" Q |", end="")
            else:
                print("   |", end="")
        print()
        print("=" * (4 * n + 1))


def compute_consumption(start: int = 4, end: int = 13) -> list[int]:
    """计算皇后数量-计算时间曲线数据"""
    solver = NQueensSolver()
    consumptions = []
    for n in range(start, end):
        solver.solve_n_queens(n)
        consumptions.append(solver.last_solved_time)
    return consumptions


def plot_consumption(consumptions: list[int], start: int = 4):
    """绘制皇后数量-计算时间开销曲线"""
    import matplotlib.pyplot as plt

    x_axis = [i for i in range(start, len(consumptions) + start)]

    plt.plot(x_axis, consumptions)
    # 懒得解决中文问题 ASCII不会受到默认字体影响
    plt.xlabel("N-queen")
    plt.ylabel("Consumption (s)")
    plt.title("Consumption curve")
    plt.savefig("./curve.png")
    plt.show()


def cmd_curve():
    plot_consumption(compute_consumption())


def cmd_test():
    theoretical_solutions = {
        1: 1,
        2: 0,
        3: 0,
        4: 2,
        5: 10,
        6: 4,
        7: 40,
        8: 92,
        9: 352,
        10: 724,
        11: 2680,
        12: 14200,
    }
    solver = NQueensSolver(MinConflictStrategy())
    error_count = 0
    for i in range(1, 13):
        solutions = solver.solve_n_queens(i)
        solutions_count = len(solutions)
        if theoretical_solutions[i] != solutions_count:
            print(f"[!] N={i} fail")
            error_count += 1
        else:
            print(f"[x] N={i} pass")
    print(f"测试完成，错误数：{error_count}")


# region IO interface


def get_input() -> int:
    """获取用户输入的N值"""
    while True:
        try:
            n = int(input("请输入N的值: "))
            if n <= 0:
                raise ValueError
            return n
        except ValueError:
            print("无效的输入，请输入一个正整数")


def show_solutions(solutions: list[list[int]]):
    solution_count = len(solutions)
    print(f"找到 {solution_count} 个解")
    while True:
        try:
            n = int(
                input(
                    f"请输入要查看的解[1-{solution_count}]（输入0退出，输入{solution_count + 1}显示全部）: "
                )
            )
            if n == 0:
                break
            elif n > 0 and n <= solution_count:
                print_board(solutions[n - 1])
            elif n == solution_count + 1:
                for idx, solution in enumerate(solutions):
                    print(f"\n\n解法{idx + 1}:")
                    print_board(solution)
            else:
                ValueError()
        except ValueError:
            print("无效的输入，请输入一个范围内的正整数")


# endregion IO interface


def main():
    n = get_input()

    solver = NQueensSolver()
    solutions = solver.solve_n_queens(n)
    print(f"求解耗时: {solver.last_solved_time:.4f}秒")

    show_solutions(solutions)


if __name__ == "__main__":
    try:
        import fire

        fire.Fire(
            {
                "solve": main,
                "test": cmd_test,
                "curve": cmd_curve,
            }
        )
    except ImportError:
        print("使用[pip install fire]来获得全功能使用")
        main()
