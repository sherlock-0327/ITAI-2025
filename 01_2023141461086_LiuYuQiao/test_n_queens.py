"""
N皇后问题测试文件
测试各种功能和边界情况
"""

import time
import unittest
from n_queens import NQueens, NQueensOptimized

class TestNQueens(unittest.TestCase):
    """N皇后问题测试类"""
    
    def setUp(self):
        """测试前置设置"""
        self.known_solutions = {
            4: 2,   # 4皇后有2个解
            5: 10,  # 5皇后有10个解
            6: 4,   # 6皇后有4个解
            7: 40,  # 7皇后有40个解
            8: 92,  # 8皇后有92个解
        }
    
    def test_basic_functionality(self):
        """测试基本功能"""
        for n, expected_count in self.known_solutions.items():
            with self.subTest(n=n):
                solver = NQueens(n)
                solutions, count = solver.solve(find_all=True)
                
                self.assertEqual(count, expected_count, 
                               f"N={n}的解数应该是{expected_count}，实际是{count}")
                self.assertEqual(len(solutions), expected_count,
                               f"N={n}的解列表长度应该是{expected_count}")
    
    def test_single_solution(self):
        """测试只查找一个解的功能"""
        for n in range(4, 9):
            with self.subTest(n=n):
                solver = NQueens(n)
                solutions, count = solver.solve(find_all=False)
                
                # 应该找到至少一个解
                self.assertGreaterEqual(count, 1, f"N={n}应该至少有一个解")
                # 解列表长度应该是1或0（但count>=1说明有解）
                self.assertLessEqual(len(solutions), 1, f"单解模式最多返回1个解")
    
    def test_bitwise_optimization(self):
        """测试位运算优化版本"""
        for n, expected_count in self.known_solutions.items():
            with self.subTest(n=n):
                solver = NQueensOptimized(n)
                solutions, count = solver.solve_bitwise(find_all=True)
                
                self.assertEqual(count, expected_count,
                               f"位运算版本N={n}的解数应该是{expected_count}，实际是{count}")
    
    def test_solution_validity(self):
        """测试解的有效性"""
        for n in range(4, 8):
            with self.subTest(n=n):
                solver = NQueens(n)
                solutions, count = solver.solve(find_all=True)
                
                for i, solution in enumerate(solutions):
                    self.assertTrue(self.is_valid_solution(solution, n),
                                  f"N={n}的第{i+1}个解无效: {solution}")
    
    def is_valid_solution(self, solution, n):
        """
        检查解是否有效
        
        Args:
            solution: 解的列表
            n: 棋盘大小
            
        Returns:
            bool: 解是否有效
        """
        if len(solution) != n:
            return False
        
        # 检查每个位置是否在有效范围内
        for col in solution:
            if col < 0 or col >= n:
                return False
        
        # 检查是否有冲突
        for i in range(n):
            for j in range(i + 1, n):
                # 检查列冲突
                if solution[i] == solution[j]:
                    return False
                # 检查对角线冲突
                if abs(solution[i] - solution[j]) == abs(i - j):
                    return False
        
        return True
    
    def test_performance_comparison(self):
        """测试性能比较"""
        n = 8  # 使用8皇后进行性能测试
        
        # 标准算法
        solver_standard = NQueens(n)
        start_time = time.time()
        solutions1, count1 = solver_standard.solve(find_all=True)
        time_standard = time.time() - start_time
        
        # 位运算优化算法
        solver_optimized = NQueensOptimized(n)
        start_time = time.time()
        solutions2, count2 = solver_optimized.solve_bitwise(find_all=True)
        time_optimized = time.time() - start_time
        
        # 验证结果一致性
        self.assertEqual(count1, count2, "两种算法的解数应该相同")
        
        # 性能提升（位运算通常更快，但不是绝对的）
        print(f"\n性能比较（N={n}）:")
        print(f"标准算法: {time_standard:.4f}秒")
        print(f"位运算优化: {time_optimized:.4f}秒")
        if time_standard > 0:
            speedup = time_standard / time_optimized
            print(f"加速比: {speedup:.2f}x")
    
    def test_board_printing(self):
        """测试棋盘打印功能"""
        solver = NQueens(4)
        solutions, count = solver.solve(find_all=False)
        
        if solutions:
            solution = solutions[0]
            
            # 测试字符棋盘打印
            board_str = solver.print_board(solution)
            self.assertIn('Q', board_str, "棋盘应该包含皇后标记'Q'")
            self.assertIn('.', board_str, "棋盘应该包含空位标记'.'")
            
            # 测试数字形式打印
            numeric_str = solver.print_board_numeric(solution)
            self.assertIn('解的向量表示', numeric_str, "应该包含向量表示")
            self.assertIn('坐标表示', numeric_str, "应该包含坐标表示")


def demo_basic_usage():
    """演示基本用法"""
    print("=" * 60)
    print("N皇后问题求解器演示")
    print("=" * 60)
    
    # 演示4皇后问题
    print("\n1. 求解4皇后问题（所有解）")
    print("-" * 30)
    
    solver = NQueens(4)
    start_time = time.time()
    solutions, count = solver.solve(find_all=True)
    end_time = time.time()
    
    print(f"解的总数: {count}")
    print(f"求解时间: {end_time - start_time:.4f}秒")
    
    print("\n所有解的详细信息:")
    for i, solution in enumerate(solutions, 1):
        print(f"\n第{i}个解:")
        print(solver.print_board(solution))
        print(solver.print_board_numeric(solution))
    
    # 演示8皇后问题（只求一个解）
    print("\n" + "=" * 60)
    print("2. 求解8皇后问题（只求一个解）")
    print("-" * 30)
    
    solver = NQueens(8)
    start_time = time.time()
    solutions, count = solver.solve(find_all=False)
    end_time = time.time()
    
    print(f"总解数: {count}")
    print(f"找到的解数: {len(solutions)}")
    print(f"求解时间: {end_time - start_time:.4f}秒")
    
    if solutions:
        print("\n找到的解:")
        print(solver.print_board(solutions[0]))
        print(solver.print_board_numeric(solutions[0]))
    
    # 演示位运算优化
    print("\n" + "=" * 60)
    print("3. 位运算优化算法演示（8皇后）")
    print("-" * 30)
    
    solver_opt = NQueensOptimized(8)
    start_time = time.time()
    solutions_opt, count_opt = solver_opt.solve_bitwise(find_all=True)
    end_time = time.time()
    time_opt = end_time - start_time
    
    print(f"解的总数: {count_opt}")
    print(f"求解时间: {time_opt:.4f}秒")
    
    # 性能对比
    solver_std = NQueens(8)
    start_time = time.time()
    solutions_std, count_std = solver_std.solve(find_all=True)
    end_time = time.time()
    time_std = end_time - start_time
    
    print(f"\n性能对比:")
    print(f"标准算法: {time_std:.4f}秒")
    print(f"位运算优化: {time_opt:.4f}秒")
    if time_std > 0:
        speedup = time_std / time_opt
        print(f"加速比: {speedup:.2f}x")


def demo_scalability():
    """演示算法可扩展性"""
    print("\n" + "=" * 60)
    print("4. 算法可扩展性演示")
    print("-" * 30)
    
    print(f"{'N':<4} {'解数':<8} {'标准算法(秒)':<15} {'位运算优化(秒)':<15} {'加速比':<8}")
    print("-" * 60)
    
    for n in range(4, 11):
        # 标准算法
        solver_std = NQueens(n)
        start_time = time.time()
        _, count_std = solver_std.solve(find_all=True)
        time_std = time.time() - start_time
        
        # 位运算优化
        solver_opt = NQueensOptimized(n)
        start_time = time.time()
        _, count_opt = solver_opt.solve_bitwise(find_all=True)
        time_opt = time.time() - start_time
        
        speedup = time_std / time_opt if time_opt > 0 else 0
        
        print(f"{n:<4} {count_std:<8} {time_std:<15.4f} {time_opt:<15.4f} {speedup:<8.2f}")
        
        # 如果时间太长，停止测试
        if max(time_std, time_opt) > 10:
            print("运行时间过长，停止测试更大的N值")
            break


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # 运行单元测试
        unittest.main(argv=[''], exit=False)
    else:
        # 运行演示
        demo_basic_usage()
        
        # 询问是否运行可扩展性测试
        choice = input("\n是否运行可扩展性测试？(y/n): ").strip().lower()
        if choice == 'y':
            demo_scalability()
        
        # 询问是否运行单元测试
        choice = input("\n是否运行单元测试？(y/n): ").strip().lower()
        if choice == 'y':
            print("\n运行单元测试...")
            unittest.main(argv=[''], exit=False)


if __name__ == "__main__":
    main()