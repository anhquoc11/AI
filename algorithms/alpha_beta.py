from algorithms import Utility
import copy

from algorithms.A_sao import Node

def alpha_beta_search(node, depth, alpha, beta, is_maximizing):
    if depth == 0 or Utility.is_terminal(node.STATE):
        return Utility.evaluate(node.STATE), None

    best_action = None
    if is_maximizing:
        max_eval = float('-inf')
        for action in Utility.get_actions(node.i, node.j, node.STATE):
            ni, nj = Utility.next_pos(node.i, node.j, action)
            new_state = copy.deepcopy(node.STATE)
            new_state[ni][nj] = 0 
            
            child = Node(ni, nj, new_state, action, node)
            eval, _ = alpha_beta_search(child, depth - 1, alpha, beta, False)
            
            if eval > max_eval:
                max_eval = eval
                best_action = action
            
            alpha = max(alpha, eval)
            if beta <= alpha:
                break 
        return max_eval, best_action
    else:
        min_eval = float('inf')
        for action in Utility.get_actions(node.i, node.j, node.STATE):
            ni, nj = Utility.next_pos(node.i, node.j, action)
            new_state = copy.deepcopy(node.STATE)
            new_state[ni][nj] = 0
            
            child = Node(ni, nj, new_state, action, node)
            eval, _ = alpha_beta_search(child, depth - 1, alpha, beta, True)
            
            if eval < min_eval:
                min_eval = eval
                best_action = action
            
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_action