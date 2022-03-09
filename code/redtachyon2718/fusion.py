params = [-1.8134498385869045, 0.22191508250395225, -1.465795354749896, 9.751323317479086, -2.3928970633951727, -3.3914284668997614, -3.8600986443237573, 1.1338265112147068]

def strategy(history, memory):
    if len(history[0]) == 0:
        ratio = 0
        alternating = 0
        hasdefdbefore = 0
        last = 0
        last2 = 0
        evil = 0
        turnnnum = 0
        response = 0
        inarow = 0
        return 1, [ratio, alternating, hasdefdbefore, last, last2, evil, response, inarow]
    else:
        ratio = memory[0] + 2 * history[1][-1] - 1
        alternating = memory[1]
        if len(history[0]) >= 3:
            alternating += 2 * int(history[1][-1] == history[1][-3] and history[1][-2] != history[1][-1]) - 1
        hasdefdbefore = 2 * int(memory[2] == 1 or history[1][-1] == 0) - 1
        last = 2 * history[1][-1] - 1
        last2 = 0
        if len(history[0]) > 1:
            last2 = 2 * history[1][-2] - 1
        evil = memory[5]
        if history[1][-1] == 0 and history[0][-1] == 1:
            evil += 1
        response = memory[6]
        if len(history[0]) > 1:
            response += 2 * int(history[1][-1] == 0 and history[0][-2] == 0) - 1
        inarow = memory[7]
        if history[1][-1] == 0:
            inarow += 1
        else:
            inarow = 0
        total = 0
        total += ratio * params[0] / len(history[0])
        total += alternating * params[1] / len(history[0])
        total += hasdefdbefore * params[2]
        total += last * params[3]
        total += last2 * params[4]
        total += evil * params[5] / len(history[0])
        total += response * params[6] / len(history[0])
        total += inarow * params[7]
        return 1 * (total >= 0), [ratio, alternating, hasdefdbefore, last, last2, evil, response, inarow]
