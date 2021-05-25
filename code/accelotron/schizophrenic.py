import random
import numpy as np


def ftft(history, memory):
    choice = 1
    if history.shape[1] >= 2 and history[1, -1] == 0 and history[1, -2] == 0:
        # We check the TWO most recent turns to see if BOTH were defections, and only then do we defect too.
        choice = 0
    return choice, None


def joss(history, memory):
    choice = 1
    if random.random() < 0.10 or (history.shape[1] >= 1 and history[1, -1] == 0):
        # Choose to defect randomly by 10% chance, OR if and only if the opponent just defected.
        choice = 0
    return choice, None


def simpleton(history, memory):
    choice = None
    if history.shape[1] == 0:  # We're on the first turn!
        choice = 1
    else:
        choice = history[0, -1]  # I will keep doing the same thing as last move!
        if history[1, -1] == 0:  # If my opponent defected last turn, I'll just do the opposite thing as my last move:
            choice = 1-choice
            
    return choice, None


def titForTat(history, memory):
    choice = 1
    if history.shape[1] >= 1 and history[1, -1] == 0:  # Choose to defect if and only if the opponent just defected.
        choice = 0
    return choice, None


def randomGuy(history, memory):
    return random.randint(0, 1), None


def grimTrigger(history, memory):
    wronged = False
    if memory is not None and memory:  # Has memory that it was already wronged.
        wronged = True
    else:  # Has not been wronged yet, historically.
        if history.shape[1] >= 1 and history[1, -1] == 0:  # Just got wronged.
            wronged = True

    if wronged:
        return 0, True
    else:
        return 1, False


# scores=np.array([0.8), threshold=np.array([0.2])
# scores=np.array([0.8, 0.7]), threshold=np.array([0.2])
# scores=np.array([0.8, 0.7, 0.9]), threshold=np.array([0.2])
# scores=np.array([0.8, 0.7, 0.9, 0.7]), threshold=np.array([0.2])
# scores=np.array([0.8, 0.7, 0.9, 0.7, 0.7]), threshold=np.array([0.3])

# scores=np.array([0.9, 0.5, 0.4, 0.2]), threshold=np.array([0.3])
# scores=np.array([0.99, 0.55, 0.42, 0.21]), threshold=np.array([0.32])


def strategy(history, memory, scores=np.array([2, 5, 1]), sanity=np.array([1])):
    # scores are np array, threshold is np array too (with one element)

    ft = ftft(history, memory)
    st = simpleton(history, memory)
    tt = titForTat(history, memory)
    gt = grimTrigger(history, memory)

    #personalities = np.array([tt[0], st[0], ft[0], gt[0]])
    personalities = np.array([tt[0], gt[0], st[0]])

    return 1 if np.mean(personalities * scores) > sanity[0] else 0, gt[1]
