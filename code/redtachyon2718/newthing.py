params = [-0.854161587643953, 2.760314128621419, -1.20348362584606, 0.8033158224598248, -0.38967842906713723, -1.4999474618681594, -0.07602295929708269, 0.049987358188995024, -0.6782360506027818, 1.3096231892099448, 0.001128829339126088, -0.22452595270089498, 0.37321467605840714]
#number of unprovoked defections / total
#c / total
#d / total
#last three moves of each player
#responsiveness
#is detective(Defected in second move, cooperated in first)
#alternating
#12 inputs in total
import numpy as n

params = n.array(params)

def strategy(history, memory):
    me = history[0]
    enemy = history[1]
    if len(me) == 0:
        attacks = 0
        c = 0
        defects = 0
        counters = 0
        alternating = 0
        detective = 0
    else:
        attacks = memory[0]
        c = memory[1]
        defects = memory[2]
        counters = memory[3]
        alternating = memory[4]
        detective = memory[5]
        if enemy[-1] == 0:
            defects += 1
            if len(me) > 1:
                if me[-1] == 1:
                    attacks += 1
                else:
                    counters += 1
            else:
                attacks += 1
        else:
            c += 1
        if len(me) > 2:
            if enemy[-1] == enemy[-3] and enemy[-1] != enemy[-2]:
                alternating += 1
    if len(enemy) == 2:
        detective = int(enemy[0] == 1 and enemy[1] == 0)
    moves = [0,0,0,0,0,0]
    for x in range(min(len(me), 3)):
        moves[x] = enemy[-x]
        moves[x + 3] = me[-x]
    div = max(1, len(enemy))
    inputvector = n.array(moves + [attacks / div, c / div, defects / div, counters / div, alternating, detective])
    perception = (inputvector * params[:-1]).sum() + params[-1]
    thought = perception >= 0
    passive = enemy.sum() != 0 or len(me) < 12
    return int(thought and passive), [attacks, c, defects, counters, alternating, detective]
