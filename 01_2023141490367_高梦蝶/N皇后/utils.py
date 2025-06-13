from typing import List


def solution_(solution: List[int], n: int) -> str:
    return '\n'.join(
        '.' * col + 'Q' + '.' * (n - col - 1)
        for col in solution
    )


def save_solutions(solutions: List[List[int]], n: int, filename: str):
    with open(filename, 'w') as f:
        for i, sol in enumerate(solutions, 1):
            f.write(f'解法{i}:\n')
            f.write(solution_(sol, n))
            f.write('\n\n')


def print_compact(solutions: List[List[int]]):
    for sol in solutions:
        print(' '.join(str(col + 1) for col in sol))
