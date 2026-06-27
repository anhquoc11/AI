import random
import copy
from config.settings import *


class DropNode:
    def __init__(self, state, action, parent):
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent

def get_valid_columns(state):
    return [c for c in range(C4_COLS) if state[0][c] == EMPTY]


def get_next_open_row(state, col):
    for r in range(C4_ROWS-1, -1, -1):
        if state[r][col] == EMPTY:
            return r
    return -1


def is_terminal_c4(state):
    return winning_move_c4(state, PLAYER_C4) or winning_move_c4(state, AI_C4) or len(get_valid_columns(state)) == 0
def winning_move_c4(state, piece):
    for c in range(C4_COLS - 3):
        for r in range(C4_ROWS):
            if state[r][c] == piece and state[r][c+1] == piece and state[r][c+2] == piece and state[r][c+3] == piece: return True
    for c in range(C4_COLS):
        for r in range(C4_ROWS - 3):
            if state[r][c] == piece and state[r+1][c] == piece and state[r+2][c] == piece and state[r+3][c] == piece: return True
    for c in range(C4_COLS - 3):
        for r in range(C4_ROWS - 3):
            if state[r][c] == piece and state[r+1][c+1] == piece and state[r+2][c+2] == piece and state[r+3][c+3] == piece: return True
    for c in range(C4_COLS - 3):
        for r in range(3, C4_ROWS):
            if state[r][c] == piece and state[r-1][c+1] == piece and state[r-2][c+2] == piece and state[r-3][c+3] == piece: return True
    return False

def evaluate_c4(state):
    if winning_move_c4(state, AI_C4): return 100
    if winning_move_c4(state, PLAYER_C4): return -100
    return 0

def minimax_drop(node, depth, is_maximizing):
    if depth == 0 or is_terminal_c4(node.STATE):
        if depth == 0 and not is_terminal_c4(node.STATE): return 0, None
        return evaluate_c4(node.STATE), None
    valid_columns = get_valid_columns(node.STATE)
    best_action = random.choice(valid_columns) if valid_columns else None

    if is_maximizing:
        max_eval = float('-inf')
        for col in valid_columns:
            row = get_next_open_row(node.STATE, col)
            new_state = copy.deepcopy(node.STATE)
            new_state[row][col] = AI_C4
            child = DropNode(new_state, col, node)
            eval, _ = minimax_drop(child, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_action = col
        return max_eval, best_action
    else:
        min_eval = float('inf')
        for col in valid_columns:
            row = get_next_open_row(node.STATE, col)
            new_state = copy.deepcopy(node.STATE)
            new_state[row][col] = PLAYER_C4
            child = DropNode(new_state, col, node)
            eval, _ = minimax_drop(child, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_action = col
        return min_eval, best_action
