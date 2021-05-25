# Zero-determinism exploitative algorithm.
# 
# P(C|CC) = 8/9
# P(C|CD) = 1/2
# P(C|DC) = 1/3
# P(C|DD) = 0

import random

def strategy(history, memory):
    p = random.random()
    if history.shape[1] == 0:
        choice = 1
    elif history[0,-1] == 1 and history[1,-1] == 1:
        if p <= 8/9:
            choice = 1
        else:
            choice = 0
    elif history[0,-1] == 1 and history[1,-1] == 0:
        if p <= 0.5:
            choice = 1
        else:
            choice = 0
    elif history[0,-1] == 0 and history[1,-1] == 1:
        if p <= 1/3:
            choice = 1
        else:
            choice = 0
    elif history[0,-1] == 0 and history[1,-1] == 0:
        choice = 0

    return choice, None