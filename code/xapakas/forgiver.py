# forgiver, based on SecondByWeiner in Axelrod's 2nd competition
#
# memory[0] is last_twelve
# memory[1] is lt_index
# memory[2] is forgive_flag (boolean)
# memory[3] is defect_padding
# memory[4] is grudge

import numpy as np

def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, [[0,0,0,0,0,0,0,0,0,0,0,0],0,False,0,0]

    # update history, lag 1.
    if history.shape[1] >= 2:
        memory[0][memory[1]] = 0
        if history[1,-2] == 0:
            memory[0][memory[1]] = 1
        memory[1] = memory[1] % 12

    if memory[2] == True:
        memory[2] = False
        if memory[4] < history.shape[0] + 1 and history[1,-1] == 0:
            # Then override
            memory[4] += 20
            return try_return(memory[0], 1), memory
        else:
            return try_return(memory[0], history[1,-1]), memory
    else:
        # see if forgive_flag should be raised
        if history[1,-1] == 0:
            memory[3] += 1
        else:
            if memory[3] % 2 == 1:
                memory[2] = True
            memory[3] = 0

        return try_return(memory[0], history[1,-1]), memory

def try_return(last_twelve, to_return):
    # logic is here to check for the defective override.
    if np.sum(last_twelve) >= 5:
        return 0
    return to_return