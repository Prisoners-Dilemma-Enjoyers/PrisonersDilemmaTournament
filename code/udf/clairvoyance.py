# Agent that uses inspect to find and run the opponent's code one round in the future.
# It assumes that the tournament runner code remains the same as it was in commit fd259dc481a34b3c869fa8ae66ea161af0d95963
# Namely the moduleA/B, memoryA/B, and playerAmove variables need to keep their names,
# and that the opponent agent is deterministic, so randomness will no doubt throw it off
#
# This is definitely cheating, but I wrote it for fun so it doesn't bother me
# if it's immediately disqualified. Though I am interested to see how it would do
# against everybody else's legal agents.
#
# Knowing the opponents next move lets us decide if the current decision will
# result in the next round being more beneficial for us. Checking more rounds
# in the future will definitely improve the result, but I'm not sure if the
# extra computation time is worth it.
#
# Obviously if you run it against itself, you'll end up with an infinite loop...
# So, uhh, don't do that.
import numpy as np
import inspect
import copy

pointsArray = [[1, 5], [0, 3]]


def strategyMove(move):
  if type(move) is str:
    defects = ["defect","tell truth"]
    return 0 if (move in defects) else 1
  else:
    # Coerce all moves to be 0 or 1 so strategies can safely assume 0/1's only
    return int(bool(move))


def strategy(history, memory):
  prev_frame = inspect.stack()[1]
  caller_locals = prev_frame.frame.f_locals

  # figure out which module the opponent is
  if caller_locals['moduleA'].__name__ == __name__:
    opponent_module_name = 'B'
  else:
    opponent_module_name = 'A'

  opponent_module = caller_locals[f'module{opponent_module_name}']
  opponent_memory = caller_locals[f'memory{opponent_module_name}']
  opponent_history = np.flip(history, 0)

  # make copy of memory in case opponent mutates their memory
  opponent_memory = copy.deepcopy(opponent_memory)

  # get opponent current move from frame if they're A
  # otherwise, run opponent strategy to get their current move
  if opponent_module_name == 'A':
    opponent_current_choice = caller_locals['playerAmove']
  else:
    opponent_current_choice, opponent_memory = opponent_module.strategy(opponent_history, opponent_memory)
  opponent_current_choice = strategyMove(opponent_current_choice)

  # create history for the next round
  next_history = np.append(
    opponent_history,
    [[opponent_current_choice], [0]],
    axis=1
  )

  # find out what the opponent will do next
  next_history[1][-1] = 0
  defect_opponent_next_move, _ = opponent_module.strategy(next_history, copy.deepcopy(opponent_memory))
  defect_opponent_next_move = strategyMove(defect_opponent_next_move)
  next_history[1][-1] = 1
  cooperate_opponent_next_move, _ = opponent_module.strategy(next_history, opponent_memory)
  cooperate_opponent_next_move = strategyMove(cooperate_opponent_next_move)

  defect_score = (
    # value of current round
    pointsArray[0][opponent_current_choice]
    # total value of the next round
    + pointsArray[0][defect_opponent_next_move]
    + pointsArray[1][defect_opponent_next_move]
  )

  cooperate_score = (
    # value of current round
    pointsArray[1][opponent_current_choice]
    # total value of the next round
    + pointsArray[0][cooperate_opponent_next_move]
    + pointsArray[1][cooperate_opponent_next_move]
  )

  return cooperate_score >= defect_score, None
