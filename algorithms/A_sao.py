from algorithms import Utility 
import copy 

class Node():
    def __init__(self,i, j, state, action, parent, g, f):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.G = g
        self.F = f

def A_sao(grid, start_i, start_j):
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0

    if Utility.count_box_cells(start_state) == 0:
        return [start_state], [],set()

    reached = {}
    visited_positions = set()
    h_start = Utility.count_box_cells(start_state) * 100 + Utility.distance_to_nearest_house(start_i, start_j, start_state)
    start_node = Node(start_i, start_j, start_state, None, None, 0, h_start)
    queue_priority = [start_node]
    visited_positions.add((start_i, start_j))
    reached[(start_i, start_j, tuple(tuple(row) for row in start_state))] = 0

    end = None
    while queue_priority:
        parent = queue_priority.pop(0)
        if Utility.count_box_cells(parent.STATE) == 0:
            end = parent
            break
        move_list = Utility.get_actions(parent.i, parent.j, parent.STATE)
        for action in move_list:
            state_child = copy.deepcopy(parent.STATE)
            i_child, j_child = Utility.next_pos(parent.i, parent.j, action)
            energy = 5 if state_child[i_child][j_child] == 2 else 1
            g_child = parent.G + energy
            state_child[i_child][j_child] = 0
            visited_positions.add((i_child, j_child))
            h_child = Utility.count_box_cells(state_child) * 100 + Utility.distance_to_nearest_house(i_child, j_child, state_child)
            child = Node(i_child, j_child, state_child, action, parent, g_child, h_child + g_child)
            key = (i_child, j_child,tuple(tuple(row) for row in state_child))
            if key not in reached or g_child < reached[key]:
                queue_priority = Utility.queue_priority_add(queue_priority, child)
                reached[key] = g_child
    path_states, actions = Utility.trace_path(end)
    return path_states, actions, visited_positions




