class ChessBoard:
    """棋盘类，处理棋盘的基本操作"""
    def __init__(self, size):
        self.size = size
        self.board = [['.'] * size for _ in range(size)]
        # 使用位运算记录占用情况
        self.cols = 0  # 列占用情况
        self.diag1 = 0  # 主对角线占用情况 (左上到右下)
        self.diag2 = 0  # 副对角线占用情况 (右上到左下)
    
    def place_queen(self, row, col):
        """在指定位置放置皇后"""
        self.board[row][col] = 'Q'
        self.cols |= (1 << col)
        self.diag1 |= (1 << (row - col + self.size - 1))
        self.diag2 |= (1 << (row + col))
    
    def remove_queen(self, row, col):
        """移除指定位置的皇后"""
        self.board[row][col] = '.'
        self.cols &= ~(1 << col)
        self.diag1 &= ~(1 << (row - col + self.size - 1))
        self.diag2 &= ~(1 << (row + col))
    
    def is_safe(self, row, col):
        """检查在指定位置放置皇后是否安全"""
        return not (
            self.cols & (1 << col) or 
            self.diag1 & (1 << (row - col + self.size - 1)) or 
            self.diag2 & (1 << (row + col))
        )
    
    def get_solution(self):
        """获取当前棋盘状态的字符串表示"""
        return [''.join(row) for row in self.board]

def solve_n_queens(n, find_all=True):
    """
    解决 N 皇后问题的主函数
    :param n: 棋盘大小和皇后数量
    :param find_all: 是否寻找所有解，False 则在找到第一个解后立即返回
    :return: 解决方案列表
    """
    validate_input(n)
    solutions = []
    board = ChessBoard(n)
    
    def backtrack(row):
        """
        回溯算法的核心实现
        :param row: 当前处理的行
        :return: 找到一个解时返回 True（仅在 find_all=False 时有效）
        """
        if row >= n:
            solutions.append(board.get_solution())
            return not find_all
        
        for col in range(n):
            if board.is_safe(row, col):
                board.place_queen(row, col)
                if backtrack(row + 1):
                    return True
                board.remove_queen(row, col)
        return False
    
    backtrack(0)
    return solutions

def validate_input(n):
    """
    验证输入参数的有效性
    :param n: 棋盘大小
    :raises: TypeError 如果n不是整数
    :raises: ValueError 如果n小于4
    """
    if not isinstance(n, int):
        raise TypeError("棋盘大小必须是整数")
    if n < 4:
        raise ValueError("N 皇后问题在 N < 4 时无解")

def print_solution(board):
    """打印单个解决方案"""
    for row in board:
        print(row)
    print()

def print_solutions(solutions, n, find_all):
    """
    打印解决方案
    :param solutions: 解决方案列表
    :param n: 棋盘大小
    :param find_all: 是否是查找所有解模式
    """
    if not solutions:
        print(f"未找到 {n} 皇后问题的解决方案")
    else:
        if find_all:
            print(f"\n找到 {len(solutions)} 个解决方案：")
            for i, solution in enumerate(solutions, 1):
                print(f"\n解决方案 #{i}:")
                print('\n'.join(solution))
                print("-" * (n * 2))
        else:
            print("\n找到一个解决方案：")
            print('\n'.join(solutions[0]))

def get_valid_n():
    """
    获取有效的棋盘大小输入
    :return: 有效的棋盘大小 N
    """
    while True:
        try:
            n = int(input("请输入棋盘大小 N（N >= 4）: "))
            if n < 4:
                print("错误：N 必须大于或等于 4，因为 N < 4 时问题无解")
                continue
            return n
        except ValueError:
            print("错误：请输入一个有效的整数")

def get_solution_mode():
    """
    获取用户选择的求解模式
    :return: 是否需要所有解
    """
    while True:
        choice = input("\n请选择求解模式：\n1. 只需要一个解\n2. 需要所有解\n请输入选项（1 或 2）: ").strip()
        if choice == "1":
            return False
        elif choice == "2":
            return True
        else:
            print("无效的选择，请输入 1 或 2")

def main():
    try:
        n = get_valid_n()
        find_all = get_solution_mode()
        
        print(f"\n求解 {n} 皇后问题..." + ("（查找所有解）" if find_all else "（查找第一个解）"))
        solutions = solve_n_queens(n, find_all)
        print_solutions(solutions, n, find_all)
                
    except (ValueError, TypeError) as e:
        print(f"错误：{str(e)}")
    except KeyboardInterrupt:
        print("\n程序已被用户中断")
    except Exception as e:
        print(f"发生未预期的错误：{str(e)}")

if __name__ == "__main__":
    main() 