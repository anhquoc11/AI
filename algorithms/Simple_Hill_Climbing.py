import copy
from algorithms import Utility

def Simple_Hill_Climbing(grid, start_i, start_j):
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    visited_positions = {(start_i, start_j)}
    h_parent = Utility.count_box_cells(start_state) * 100 + Utility.distance_to_nearest_house(start_i, start_j, start_state)
    if h_parent == 0:
        return [start_state], [],set()
    state_parent = start_state
    i_parent, j_parent = start_i, start_j
    path_states = [state_parent]
    actions = []
    while True:
        found_better = False
        move_list = Utility.get_actions(i_parent,j_parent,state_parent)
        for action in move_list:
            i_child, j_child = Utility.next_pos(i_parent, j_parent, action)
            state_child = copy.deepcopy(state_parent)
            if state_child[i_child][j_child] == 5: state_child[i_child][j_child] = 0
            visited_positions.add((i_child, j_child))
            h_child = Utility.count_box_cells(state_child) * 100 + Utility.distance_to_nearest_house(i_child, j_child, state_child)
            if h_child < h_parent:
                h_parent = h_child
                state_parent = state_child
                i_parent, j_parent = i_child, j_child
                actions.append(action)
                path_states.append(state_child)
                found_better = True
                break
        if not found_better:
            break
        if h_parent == 0:
            return path_states, actions, visited_positions
    return [], [], visited_positions

