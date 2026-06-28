import copy 

class CaroNode:
    def __init__(self, state, action, parent):
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        
def get_actions_caro(state):
    return [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0]

def check_winner_caro(state):
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2] and state[i][0] != 0: return state[i][0]
        if state[0][i] == state[1][i] == state[2][i] and state[0][i] != 0: return state[0][i]
    if state[0][0] == state[1][1] == state[2][2] and state[0][0] != 0: return state[0][0]
    if state[0][2] == state[1][1] == state[2][0] and state[0][2] != 0: return state[0][2]
    return 0

def is_terminal_caro(state):
    return check_winner_caro(state) != 0 or not get_actions_caro(state)

def evaluate_caro(state):
    winner = check_winner_caro(state)
    if winner == 2: return 10
    if winner == 1: return -10
    return 0

def alpha_beta_caro(node, depth, alpha, beta, is_maximizing):
    if depth == 0 or is_terminal_caro(node.STATE):
        return evaluate_caro(node.STATE), None
    best_action = None
    if is_maximizing:
        max_eval = float('-inf')
        for action in get_actions_caro(node.STATE):
            new_state = copy.deepcopy(node.STATE)
            new_state[action[0]][action[1]] = 2
            eval, _ = alpha_beta_caro(CaroNode(new_state, action, node), depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_action = action
            alpha = max(alpha, eval)
            if beta <= alpha: break
        return max_eval, best_action
    else:
        min_eval = float('inf')
        for action in get_actions_caro(node.STATE):
            new_state = copy.deepcopy(node.STATE)
            new_state[action[0]][action[1]] = 1
            eval, _ = alpha_beta_caro(CaroNode(new_state, action, node), depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_action = action
            beta = min(beta, eval)
            if beta <= alpha: break
        return min_eval, best_action