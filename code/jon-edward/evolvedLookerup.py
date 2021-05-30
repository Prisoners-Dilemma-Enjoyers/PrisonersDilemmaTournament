C, D = 1, 0


def get_lookup_table() -> dict:

    def pad_to(string, length):
        if len(string) < length:
            return ("0"*(length - len(string))) + string
        else:
            return string
    
    pattern = [
        C, D, D, C, D, C, D, D,
        C, D, D, D, C, D, D, D,
        D, D, C, D, C, D, C, C,
        C, D, D, C, C, D, C, D,
        D, D, C, C, C, C, C, D,
        D, D, C, D, D, D, D, D,
        D, D, D, D, C, C, D, D,
        C, D, D, D, C, C, C, D
    ]

    lookup_str = [pad_to(bin(k)[2:], 6) for k in range(64)][::-1]
    lookup = {
        (
            (int(s[:2][0]), int(s[:2][1])),
            (int(s[2:4][0]), int(s[2:4][1])),
            (int(s[-2:][0]), int(s[-2:][1]))
        ): p for s, p in zip(lookup_str, pattern)
    }
    return lookup


def strategy(history, memory):

    initial_actions = (C, C)

    if not memory:
        memory = get_lookup_table()

    turn_number = history.shape[1]

    if turn_number < 2:

        return initial_actions[turn_number], memory

    else:
        lst_history = list(history)

        self_history = list(lst_history[0])

        opponent_history = list(lst_history[1])

        lookup_reference = (
            tuple(self_history[-2:]),
            tuple(opponent_history[-2:]),
            tuple(opponent_history[:2])
        )

        return memory[lookup_reference], memory
