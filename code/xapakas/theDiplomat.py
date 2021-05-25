# the version I made 3 days ago that's somehow better than what I have now

import random

def strategy(history, memory):
    deadlockThreshold = 3
    exploiterThreshold = 8

    if memory == None:
        memory = [0,0,0,0]
        choice = 1

    elif memory[2] != 0: # another coop on long-term forgivness
        choice = 1
        memory[2] = 0

    # check if a deadlock is detected.
    elif memory[0] >= deadlockThreshold:
        # stay silent twice as a truce attempt
        choice = 1

        if memory[0] == deadlockThreshold:
            memory[0] += 1
        else:
            memory[0] = 0
    else:
        if history.shape[1] >= 2 and history.shape[1] <= 20:
            # modify the exploiter counter
            if history[1,-1] == 1 and history[1,-2] == 1:
                # opponent cooperates twice; decrement
                memory[1] -= 1
            if history[1,-1] != history[1,-2]:
                # opponent changes move; increment
                memory[1] += 1
            if history[1,-1] != history[0,-2]:
                # opponent moves in a non-TFT fashion; increment
                memory[1] += 1

        if memory[1] >= exploiterThreshold:
            # tell truth indefinitely
            # (exploiter counter will never fall below threshold)
            choice = 0
        else:
            if history[1,-1] == 0: # tit-for-tat
                choice = 0
            else:
                choice = 1

            # prepare for possible deadlock if switching
            # moves, or reset if choosing the same move
            if history.shape[1] >= 2 and history[1,-1] != history[1,-2]:
                memory[0] += 1
            else:
                memory[0] = 0

    if history.shape[1] >= 1 and history[0,-1] == 0 and history[1,-1] == 0 \
       and choice == 0:
        # attempt to break defection chain with double coop
        if memory[1] < exploiterThreshold and random.random() <= 1/3:
            choice = 1
            memory[2] = 1

    return choice, memory