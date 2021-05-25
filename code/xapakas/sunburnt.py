# So named as I am insufferably sunburnt right now

import random

def strategy(history, memory):
    DEADLOCK_THRESHOLD = 3
    RANDOM_THRESHOLD = 8

    if memory == None:
        return 1, [0,0,0,0,0,0,0]
    
    # update Cooperation counts during blockade/non-blockade rounds
    if memory[1] < RANDOM_THRESHOLD and memory[6] != 2: # non-blockade round
        memory[3] += 1
        if history[1,-1] == 1: # opponent Coop
            memory[2] += 1
    else: # blockade round
        memory[5] += 1
        if history[1,-1] == 1: # opponent Coop
            memory[4] += 1

    # if there are backlogged Cooperations after a blockade lift, continue Coops
    if memory[6] != 0:
        choice = 1
        memory[6] -= 1

    # check if a deadlock is detected.
    elif memory[0] >= DEADLOCK_THRESHOLD:
        # stay silent twice as a truce attempt
        choice = 1

        if memory[0] == DEADLOCK_THRESHOLD:
            memory[0] += 1
        else:
            memory[0] = 0
    else:
        if history.shape[1] >= 2:
            # modify randomness counter
            if history[1,-1] == 1 and history[1,-2] == 1:
                # opponent Cooperates twice; decrement
                memory[1] -= 1
            if history[1,-1] != history[1,-2]:
                # opponent changes move; increment
                memory[1] += 1
            if history[1,-1] != history[0,-2]:
                # opponent moves in non-tit-for-tat fashion; increment
                memory[1] += 1

        if memory[1] >= RANDOM_THRESHOLD:
            # start/continue blockade (indefinite defection)
            # (randomness counter cannot fall below threshold during blockade)
            choice = 0

            # consider lifting blockade every 30 rounds UPDATE 30 -> 20
            if memory[5] != 0 and memory[5] % 20 == 0:
                if (memory[4] > 0 and memory[3] > 0 and memory[5] > 0 and \
                   (memory[2] / memory[3]) / (memory[4] / memory[5]) >= 2) or \
                   memory[4] == 0 and memory[2] != 0:
                    # lift blockade
                    memory[1] = 0
                    memory[6] = 2 # Coop over next two rounds
                    choice = 1

                    # reset counters
                    memory[2] = 0
                    memory[3] = 0
                    memory[4] = 0
                    memory[5] = 0
        else:
            # GTFT (tit-for-tat first 13 rounds)
            if history[1,-1] == 1:
                choice = 1
            else:
                if random.random() <= 1/3 and history.shape[1] > 13:
                    choice = 1
                else:
                    choice = 0

            # update the deadlock counter. increment if opponent changed their
            # move, decrement if opponent made the same move twice in a row.
            if history.shape[1] >= 2 and history[1,-1] != history[1,-2]:
                memory[0] += 1
            else:
                memory[0] = 0

    return choice, memory