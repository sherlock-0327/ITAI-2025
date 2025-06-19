"""
N皇后问题解决方案
使用回溯算法和多种优化技术求解N皇后问题
"""

import time
import sys
from typing import List, Tuple, Set
import os

class NQueens:
    """N皇后问题求解器"""
    
    def __init__(self, n: int):
        """
        初始化N皇后求解器
        
        Args:
            n: 棋盘大小
        """
        self.n = n
        self.solutions = []
        self.solution_count = 0
        
        # 优化数据结构：使用集合标记已占用的列和对角线
        self.cols = set()           # 已占用的列
        self.diag1 = set()          # 已占用的主对角线 (row - col)
        self.diag2 = set()          # 已占用的副对角线 (row + col)
        
    def is_safe(self, row: int, col: int) -> bool:
        """
        检查在(row, col)位置放置皇后是否安全
        使用集合进行O(1)时间复杂度的冲突检测
        
        Args:
            row: 行位置
            col: 列位置
            
        Returns:
            bool: 是否安全
        """
        return (col not in self.cols and 
                (row - col) not in self.diag1 and 
                (row + col) not in self.diag2)
    
    def place_queen(self, row: int, col: int):
        """
        在(row, col)位置放置皇后，更新标记集合
        
        Args:
            row: 行位置
            col: 列位置
        """
        self.cols.add(col)
        self.diag1.add(row - col)
        self.diag2.add(row + col)
    
    def remove_queen(self, row: int, col: int):
        """
        移除(row, col)位置的皇后，更新标记集合
        
        Args:
            row: 行位置
            col: 列位置
        """
        self.cols.remove(col)
        self.diag1.remove(row - col)
        self.diag2.remove(row + col)
    
    def backtrack(self, row: int, board: List[int], find_all: bool = True) -> bool:
        """
        回溯算法求解N皇后问题
        
        Args:
            row: 当前处理的行
            board: 棋盘状态，board[i]表示第i行皇后的列位置
            find_all: 是否查找所有解
            
        Returns:
            bool: 是否找到解
        """
        # 基本情况：所有皇后都已放置
        if row == self.n:
            self.solution_count += 1
            if find_all:
                self.solutions.append(board[:])  # 深拷贝当前解
            return True
        
        found = False
        # 尝试在当前行的每一列放置皇后
        for col in range(self.n):
            if self.is_safe(row, col):
                # 放置皇后
                board[row] = col
                self.place_queen(row, col)
                
                # 递归处理下一行
                if self.backtrack(row + 1, board, find_all):
                    found = True
                    if not find_all:  # 只需要一个解
                        return True
                
                # 回溯：移除皇后
                self.remove_queen(row, col)
        
        return found
    
    def solve(self, find_all: bool = True) -> Tuple[List[List[int]], int]:
        """
        求解N皇后问题
        
        Args:
            find_all: 是否查找所有解
            
        Returns:
            Tuple[List[List[int]], int]: (解的列表, 解的总数)
        """
        # 重置状态
        self.solutions = []
        self.solution_count = 0
        self.cols.clear()
        self.diag1.clear()
        self.diag2.clear()
        
        # 开始回溯
        board = [-1] * self.n
        self.backtrack(0, board, find_all)
        
        return self.solutions, self.solution_count
    
    def print_board(self, solution: List[int]) -> str:
        """
        打印棋盘解
        
        Args:
            solution: 解的列表，solution[i]表示第i行皇后的列位置
            
        Returns:
            str: 棋盘的字符串表示
        """
        result = []
        result.append("+" + "-" * (2 * self.n - 1) + "+")
        
        for row in range(self.n):
            line = "|"
            for col in range(self.n):
                if solution[row] == col:
                    line += "Q"
                else:
                    line += "."
                if col < self.n - 1:
                    line += " "
            line += "|"
            result.append(line)
        
        result.append("+" + "-" * (2 * self.n - 1) + "+")
        return "\n".join(result)
    
    def print_board_numeric(self, solution: List[int]) -> str:
        """
        打印棋盘解（数字形式）
        
        Args:
            solution: 解的列表
            
        Returns:
            str: 棋盘的数字表示
        """
        result = []
        result.append(f"解的向量表示: {solution}")
        result.append("坐标表示: " + ", ".join([f"({i}, {solution[i]})" for i in range(self.n)]))
        return "\n".join(result)


class NQueensOptimized(NQueens):
    """N皇后问题求解器（位运算优化版本）"""
    
    def __init__(self, n: int):
        super().__init__(n)
        self.all_ones = (1 << n) - 1  # n个1的二进制数
    
    def backtrack_bitwise(self, row: int, cols: int, diag1: int, diag2: int, 
                         board: List[int], find_all: bool = True) -> bool:
        """
        使用位运算优化的回溯算法
        
        Args:
            row: 当前行
            cols: 已占用列的位掩码
            diag1: 已占用主对角线的位掩码
            diag2: 已占用副对角线的位掩码
            board: 棋盘状态
            find_all: 是否查找所有解
            
        Returns:
            bool: 是否找到解
        """
        if row == self.n:
            self.solution_count += 1
            if find_all:
                self.solutions.append(board[:])
            return True
        
        # 计算当前行可放置位置的位掩码
        available = self.all_ones & ~(cols | diag1 | diag2)
        found = False
        
        while available:
            # 获取最右边的1的位置
            pos = available & -available
            available &= available - 1  # 清除最右边的1
            
            # 计算列位置
            col = bin(pos).count('0') - 1
            board[row] = col
            
            # 递归处理下一行
            if self.backtrack_bitwise(row + 1, 
                                    cols | pos,
                                    (diag1 | pos) << 1,
                                    (diag2 | pos) >> 1,
                                    board, find_all):
                found = True
                if not find_all:
                    return True
        
        return found
    
    def solve_bitwise(self, find_all: bool = True) -> Tuple[List[List[int]], int]:
        """
        使用位运算优化的求解方法
        
        Args:
            find_all: 是否查找所有解
            
        Returns:
            Tuple[List[List[int]], int]: (解的列表, 解的总数)
        """
        self.solutions = []
        self.solution_count = 0
        
        board = [-1] * self.n
        self.backtrack_bitwise(0, 0, 0, 0, board, find_all)
        
        return self.solutions, self.solution_count


def get_n_from_input() -> int:
    """
    从用户输入获取N值
    
    Returns:
        int: 棋盘大小N
    """
    while True:
        try:
            n = int(input("请输入棋盘大小N（N >= 4）: "))
            if n < 4:
                print("N必须大于等于4，请重新输入！")
                continue
            return n
        except ValueError:
            print("请输入有效的整数！")


def get_n_from_file(filename: str) -> int:
    """
    从文件读取N值
    
    Args:
        filename: 文件名
        
    Returns:
        int: 棋盘大小N
        
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件内容无效
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            n = int(f.read().strip())
            if n < 4:
                raise ValueError(f"N必须大于等于4，当前值为{n}")
            return n
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {filename} 不存在")
    except ValueError as e:
        raise ValueError(f"文件内容无效: {e}")


def interactive_mode():
    """交互式模式主函数"""
    print("=" * 50)
    print("N皇后问题求解器")
    print("=" * 50)
    
    # 选择输入方式
    while True:
        print("\n请选择输入方式:")
        print("1. 键盘输入")
        print("2. 文件输入")
        choice = input("请选择 (1-2): ").strip()
        
        if choice == '1':
            n = get_n_from_input()
            break
        elif choice == '2':
            filename = input("请输入文件名: ").strip()
            try:
                n = get_n_from_file(filename)
                print(f"从文件 {filename} 读取到 N = {n}")
                break
            except (FileNotFoundError, ValueError) as e:
                print(f"错误: {e}")
                continue
        else:
            print("无效选择，请重新输入！")
    
    # 选择求解模式
    while True:
        print(f"\n求解 {n} 皇后问题:")
        print("1. 查找所有解")
        print("2. 只查找一个解")
        print("3. 使用位运算优化（查找所有解）")
        print("4. 使用位运算优化（只查找一个解）")
        mode = input("请选择模式 (1-4): ").strip()
        
        if mode in ['1', '2', '3', '4']:
            break
        else:
            print("无效选择，请重新输入！")
    
    # 求解
    find_all = mode in ['1', '3']
    use_bitwise = mode in ['3', '4']
    
    print(f"\n开始求解 {n} 皇后问题...")
    start_time = time.time()
    
    if use_bitwise:
        solver = NQueensOptimized(n)
        solutions, count = solver.solve_bitwise(find_all)
        print("使用位运算优化算法")
    else:
        solver = NQueens(n)
        solutions, count = solver.solve(find_all)
        print("使用标准回溯算法")
    
    end_time = time.time()
    solve_time = end_time - start_time
    
    # 输出结果
    print(f"\n求解完成！")
    print(f"总解数: {count}")
    print(f"求解时间: {solve_time:.4f} 秒")
    
    if solutions:
        print(f"\n找到的解数: {len(solutions)}")
        
        # 询问是否显示解
        show_solutions = input("\n是否显示解的详细信息？(y/n): ").strip().lower()
        if show_solutions == 'y':
            display_mode = input("选择显示模式 (1-字符棋盘, 2-数字形式, 3-两种都显示): ").strip()
            
            for i, solution in enumerate(solutions, 1):
                print(f"\n第 {i} 个解:")
                if display_mode in ['1', '3']:
                    print(solver.print_board(solution))
                if display_mode in ['2', '3']:
                    print(solver.print_board_numeric(solution))
                
                # 如果解太多，询问是否继续
                if i >= 5 and i < len(solutions):
                    continue_show = input(f"\n已显示 {i} 个解，是否继续显示剩余 {len(solutions) - i} 个解？(y/n): ").strip().lower()
                    if continue_show != 'y':
                        break


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 命令行模式
        try:
            n = int(sys.argv[1])
            if n < 4:
                print("N必须大于等于4")
                return
            
            solver = NQueens(n)
            start_time = time.time()
            solutions, count = solver.solve(True)
            end_time = time.time()
            
            print(f"{n} 皇后问题的解数: {count}")
            print(f"求解时间: {end_time - start_time:.4f} 秒")
            
        except ValueError:
            print("请输入有效的整数")
    else:
        # 交互式模式
        interactive_mode()


if __name__ == "__main__":
    main()