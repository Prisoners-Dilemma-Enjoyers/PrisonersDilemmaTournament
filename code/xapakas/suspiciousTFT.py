# tit-for-tat that starts off defecting. How good is your conflict-resolution?

def strategy(history, memory):
    choice = 0
    if history.shape[1] >= 1 and history[1,-1] == 1:
        choice = 1
    return choice, None
