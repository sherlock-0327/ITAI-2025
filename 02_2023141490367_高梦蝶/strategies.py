import numpy as np

def random_strategy(prisoner_num, boxes, max_attempts):
    attempts = np.random.choice(len(boxes), size=max_attempts, replace=False)
    return any(boxes[i] == prisoner_num for i in attempts)

def loop_strategy(prisoner_num, boxes, max_attempts):
    current = prisoner_num - 1
    for _ in range(max_attempts):
        if boxes[current] == prisoner_num:
            return True
        current = boxes[current] - 1
    return False