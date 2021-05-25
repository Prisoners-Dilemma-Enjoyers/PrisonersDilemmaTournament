# Generous Zero-Determinism algorithm that won a 2012 ZD-tournament.

import random

def strategy(history, memory):
    p = random.random()
    if history.shape[1] == 0:
        choice = 1
    elif history[0,-1] == 1 and history[1,-1] == 1:
        choice = 1
    elif history[0,-1] == 1 and history[1,-1] == 0:
        if p <= 0.125:
            choice = 1
        else:
            choice = 0
    elif history[0,-1] == 0 and history[1,-1] == 1:
        choice = 1
    elif history[0,-1] == 0 and history[1,-1] == 0:
        if p <= 0.25:
            choice = 1
        else:
            choice = 0
            
    return choice, None