import unittest
import time
import csv
from nqueen import solve_n_queens

class TestNQueen(unittest.TestCase):
    def test_basic_cases(self):
        test_cases = {
            4: 2,
            5: 10,
            8: 92
        }
        for n, expected in test_cases.items():
            with self.subTest(n=n):
                start = time.time()
                solutions = solve_n_queens(n)
                self.assertEqual(len(solutions), expected)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            solve_n_queens(3)

def benchmark():
    with open('performance.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['N', 'Time(s)', 'Solutions'])
        
        for n in range(4, 13):
            start = time.time()
            solutions = solve_n_queens(n)
            duration = time.time() - start
            writer.writerow([n, duration, len(solutions)])
            print(f'N={n}: {len(solutions)} solutions, {duration:.3f}s')

if __name__ == '__main__':
    print('运行单元测试...')
    unittest.main(exit=False)
    
    print('\n执行性能测试...')
    benchmark()
    print('结果已保存到performance.csv')