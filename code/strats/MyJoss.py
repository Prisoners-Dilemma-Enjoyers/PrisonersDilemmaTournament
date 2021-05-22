import random

# Variant of Tit For Tat that randomly defects to try to take advantage
# of overly forgiving opponents.

# Reminder: For the history array, "cooperate" = 1, "defect" = 0
def TickedOffCopycat(history, memory):
    round = history.shape[1]
    if round == 0:
        return "cooperate", True
    if round == 1:  
        if history[1,-1] == 0:
            return "defect", True
        else:
            return "cooperate", True
    if history[1,-1] == 0 or history [1, -2] == 0:
        return "defect", True
    return "cooperate", True

def strategy(history, memory):
    round = history.shape[1]
    if memory == True:
        return TickedOffCopycat(history, memory)
    if round >= 12:
        sin = 0
        for i in range (1, 13):
            if history[1, -i] == 0:
                sin+=1
        if sin>=4:
            return TickedOffCopycat(history, memory)

    if round%6 == 0:
         return "cooperate", False
    if round%6 == 1:
         return "cooperate", False
    if round%6 == 2:
         return "cooperate", False
    if round%6 == 3:
         return "defect", False
    if round%6 == 4:
         return "cooperate", False
    if round%6 == 5:
         return "defect", False

