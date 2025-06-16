import random
import time
from typing import List, Tuple
import numpy as np

def calculate_conflicts(individual: List[int]) -> int:
#计算个体的冲突数目
    n = len(individual)
    conflicts = 0
    
    # 检查行冲突（每个数字只能出现一次）
    conflicts += n - len(set(individual))
    
    # 检查斜线冲突
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(individual[i] - individual[j]):
                conflicts += 1
                
    return conflicts

def fitness(individual: List[int]) -> float:
#计算适应度值
    conflicts = calculate_conflicts(individual)
    return 1.0 / (1.0 + conflicts)  # 将冲突数转换为适应度值

def order_crossover(parent1: List[int], parent2: List[int]) -> List[int]:
#顺序交叉
    n = len(parent1)
    # 随机选择交叉点
    cx1, cx2 = sorted(random.sample(range(n), 2))
    
    # 从parent1复制中间段
    child = [-1] * n
    child[cx1:cx2] = parent1[cx1:cx2]
    
    # 从parent2填充剩余位置
    remaining = [x for x in parent2 if x not in child[cx1:cx2]]
    j = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = remaining[j]
            j += 1
            
    return child

def mutate(individual: List[int], mutation_rate: float) -> List[int]:
#变异操作
    if random.random() < mutation_rate:
        n = len(individual)
        i, j = random.sample(range(n), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def select_parents(population: List[List[int]], fitnesses: List[float], num_parents: int) -> List[List[int]]:
#锦标赛
    parents = []
    for _ in range(num_parents):
        # 随机选择3个个体进行锦标赛
        tournament = random.sample(list(zip(population, fitnesses)), 3)
        # 选择适应度最高的个体
        winner = max(tournament, key=lambda x: x[1])[0]
        parents.append(winner)
    return parents

def genetic_algorithm(n: int, pop_size: int = 100, max_generations: int = 1000) -> Tuple[List[int], float]:
#遗传算法
    start_time = time.time()
    
    # 初始化种群
    population = [random.sample(range(n), n) for _ in range(pop_size)]
    best_fitness = 0
    best_solution = None
    generation_without_improvement = 0
    mutation_rate = 0.1  # 初始变异率
    
    for generation in range(max_generations):
        # 计算适应度
        fitnesses = [fitness(ind) for ind in population]
        
        # 更新最优解
        max_fitness = max(fitnesses)
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_solution = population[fitnesses.index(max_fitness)]
            generation_without_improvement = 0
        else:
            generation_without_improvement += 1
        
        # 自适应变异率
        if generation_without_improvement > 20:
            mutation_rate = min(0.5, mutation_rate * 1.1)
        else:
            mutation_rate = max(0.01, mutation_rate * 0.99)
        
        # 检查是否找到解
        if best_fitness == 1.0:  # 无冲突
            print(f"找到解！在第 {generation} 代")
            break
            
        # 选择父代
        parents = select_parents(population, fitnesses, pop_size // 2)
        
        # 精英保留
        elite_size = pop_size // 10
        elite = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)[:elite_size]
        elite = [ind for ind, _ in elite]
        
        # 生成新种群
        new_population = elite.copy()
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(parents, 2)
            child = order_crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
            
        population = new_population
        
        # 每100代打印一次进度
        if generation % 100 == 0:
            print(f"第 {generation} 代，当前最优适应度: {best_fitness:.4f}，变异率: {mutation_rate:.4f}")
    
    end_time = time.time()
    running_time = end_time - start_time
    
    if best_solution is None:
        print("未找到解")
        return None, running_time
        
    return best_solution, running_time

def print_board(solution: List[int]) -> None:
#可视化解集
    n = len(solution)
    for row in range(n):
        line = ['.'] * n
        line[solution[row]] = 'Q'
        print(' '.join(line))

def main():
    # 测试不同规模的N皇后问题
    n_values = [8, 12, 16]
    for n in n_values:
        print(f"\n求解 {n} 皇后问题：")
        solution, running_time = genetic_algorithm(n, pop_size=200, max_generations=2000)
        if solution:
            print(f"运行时间: {running_time:.2f} 秒")
            print("解：")
            print_board(solution)
        else:
            print(f"运行时间: {running_time:.2f} 秒")
            print("未找到解")

if __name__ == "__main__":
    main()