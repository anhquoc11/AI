from algorithms import Utility
import copy

class Node():
    def __init__(self, i, j, state, action, parent):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent

def evaluate(state):
    return 1 if Utility.is_terminal(state) else 0

def minimax(node, depth, is_maximizing):
    if depth == 0 or Utility.is_terminal(node.STATE):
        return evaluate(node.STATE), None

    best_action = None
    if is_maximizing:
        max_eval = float('-inf')
        actions = Utility.get_actions(node.i, node.j, node.STATE)
        for action in actions:
            ni, nj = Utility.next_pos(node.i, node.j, action)
            new_state = copy.deepcopy(node.STATE)
            new_state[ni][nj] = 0
            
            child = Node(ni, nj, new_state, action, node)
            eval, _ = minimax(child, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_action = action
        return max_eval, best_action
    else:
        min_eval = float('inf')
        actions = Utility.get_actions(node.i, node.j, node.STATE)
        for action in actions:
            ni, nj = Utility.next_pos(node.i, node.j, action)
            new_state = copy.deepcopy(node.STATE)
            new_state[ni][nj] = 0
            
            child = Node(ni, nj, new_state, action, node)
            eval, _ = minimax(child, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_action = action
        return min_eval, best_action