# Code by >>> ACCELOTRON >>> for carykh's $1,000 Coding Tournament
import numpy as np


def strategy(history, memory):
    # init memory
    if memory is None:
        memory = {
            'friendly': True,
            'd_timer': 0,
            'd_time': 10,
            'ignore_last_action': False,
            'has_second_chance': True,
            'op_scores': np.array([]),
            'my_scores': np.array([])
        }

    if memory['d_timer'] > 0:
        # if timer is on -> ignore opponent
        memory['d_timer'] = memory['d_timer'] - 1
        return 0, memory
    else:
        if memory['friendly']:
            if history.shape[1] >= 1:
                if history[1, -1] == 0 and not memory['ignore_last_action']:
                    # I won't hurt you, unless you cheat
                    memory['friendly'] = False
                    memory['d_timer'] = memory['d_time'] - 1
                    return 0, memory
                else:
                    memory['ignore_last_action'] = False
                    return 1, memory  # do not cheat while friendly
            else:
                return 1, memory  # cooperate on first round
        else:
            # Check opponent and exploit if he is random.
            if memory['has_second_chance']:
                memory['has_second_chance'] = False

                opp_act = history[1][-memory['d_time']::]
                personal_profile = np.mean(opp_act * 4 + 1)
                clusters_n = sum([1 if opp_act[i] != opp_act[i + 1] else 0 for i in range(len(opp_act) - 1)]) + 1

                if personal_profile > 1.8 or personal_profile == 1 or clusters_n > 2:
                    # too much or no cooperation
                    return 0, memory
                else:
                    # Tries to cooperate second time.
                    memory['friendly'] = True
                    # this ignores one defect from opponent
                    # I made it so tft-based strategies could cooperate back
                    # Without causing echo (C-D-C-D-C-D-...)
                    memory['ignore_last_action'] = True
                    return 1, memory
            else:
                # Yr dead 4 me bruh
                return 0, memory


if __name__ == '__main__':
    print('Starting test mode!')

    def getVisibleHistory(history, player, turn):
        historySoFar = history[:, :turn].copy()
        if player == 1:
            historySoFar = np.flip(historySoFar, 0)
        return historySoFar

    cm_memory = None
    game_length = int(input())
    game_history = np.zeros((2, game_length), dtype=int)

    for i in range(0, game_length):
        cm_move, cm_memory = strategy(getVisibleHistory(game_history, 0, i), cm_memory)
        test_move = int(input())
        game_history[0, i] = cm_move
        game_history[1, i] = test_move
        print('cm ->    ', game_history[0], '\ntester ->', game_history[1], '\nlast cm move', cm_move)

