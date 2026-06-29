
import random
from algorithms.alpha_beta import *
from algorithms.minimax import *

def update_caro(caro_board,current_difficulty_idx,DIFFICULTY_LEVELS,fuel):
    opt_prob = 1.0 
    if DIFFICULTY_LEVELS[current_difficulty_idx] == "DỄ": opt_prob = 0.20 
    elif DIFFICULTY_LEVELS[current_difficulty_idx] == "TRUNG BÌNH": opt_prob = 0.70 
            
    if random.random() < opt_prob:
        score, best_move = alpha_beta_caro(CaroNode(caro_board, None, None), 9, float('-inf'), float('inf'), True)
    else:
        available_moves = get_actions_caro(caro_board)
        best_move = random.choice(available_moves) if available_moves else None

    if best_move: caro_board[best_move[0]][best_move[1]] = 2
    caro_player_turn = True
    return caro_player_turn, fuel
