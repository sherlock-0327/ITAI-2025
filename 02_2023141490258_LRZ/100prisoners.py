import random


def simulate_random_choice(prisoners, chances): #随机策略模拟
    box_content = list(range(1, prisoners + 1)) 
    random.shuffle(box_content)
    for i in range(1, prisoners + 1):
        found = False
        for _ in range(chances):
            box_number = random.randint(1, prisoners) 
            if box_content[box_number - 1] == i: 
                found = True
                break
        if not found:
            return False
    return True

def simulate_chain_choice(prisoners, chances): #链式策略模拟
    box_content = list(range(1, prisoners + 1)) 
    random.shuffle(box_content)
    for i in range(1, prisoners + 1):
        current_box = i
        found = False
        for _ in range(chances):
            if box_content[current_box - 1] == i:
                found = True
                break
            current_box = box_content[current_box - 1] 
        if not found:
            return False
    return True

prisoners = int(input("Enter the number of prisoners (1-100): "))
chances = int(input("Enter the number of chances each prisoner has (1-100): "))
simulate_times = int(input("Enter the number of simulations to run: "))

random_success_count = 0
chain_success_count = 0

for _ in range(simulate_times):
    if simulate_random_choice(prisoners, chances):
        random_success_count += 1
    if simulate_chain_choice(prisoners, chances):
        chain_success_count += 1

print(f"Random choice success rate: {random_success_count / simulate_times * 100:.2f}%")
print(f"Chain choice success rate: {chain_success_count / simulate_times * 100:.2f}%")