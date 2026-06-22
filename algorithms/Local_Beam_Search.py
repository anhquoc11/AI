from algorithms import Utility
import copy 

class Node():
    def __init__(self,i, j, state, action, parent, h):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.H = h

def Local_Beam_Search(grid, start_i, start_j):
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    h_parent = Utility.count_box_cells(start_state) * 100 + Utility.distance_to_nearest_house(start_i, start_j, start_state)
    if h_parent == 0:
        return [start_state], [], set()
    
    start_node = Node(start_i, start_j, start_state, None, None, h_parent)
    queue_priority = [start_node]
    beam = 3
    visited_positions = set()
    visited_positions.add((start_i, start_j))
    
    while queue_priority:
        children = []
        count_node = min(len(queue_priority), beam)
        for index in range(count_node):
            parent = queue_priority[index]
            move_list = Utility.get_actions(parent.i, parent.j, parent.STATE)
            for action in move_list:
                state_child = copy.deepcopy(parent.STATE)
                i_child, j_child = Utility.next_pos(parent.i, parent.j, action)
                state_child[i_child][j_child] = 0
                visited_positions.add((i_child, j_child))
                h_child = Utility.count_box_cells(state_child) * 100 + Utility.distance_to_nearest_house(i_child, j_child, state_child)
                child = Node(i_child, j_child, state_child, action, parent, h_child)
                if h_child == 0:
                    path_states, actions = Utility.trace_path(child)
                    return path_states, actions, visited_positions
                children = Utility.queue_priority_add_greedy(children, child)
        k = min(len(children), beam)
        queue_priority = children[:k]
    
    return [], [], visited_positions


