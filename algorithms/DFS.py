from algorithms import Utility
import copy 

class Node():
    def __init__(self,i, j, state, action, parent):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent

def DFS(grid, start_i, start_j):
    stack = []
    reached = set()
    visited_positions = set()
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    visited_positions.add((start_i, start_j))
    if Utility.count_box_cells(start_state) == 0:
        return [start_state], [],set()
    stack.append(Node(start_i,start_j,start_state,None,None))
    reached.add((start_i,start_j,tuple(tuple(row) for row in start_state)))
    end = None 
    while stack:
        parent = stack.pop()
        move_list = Utility.get_actions(parent.i,parent.j,parent.STATE)
        for action in move_list:
            state_child = copy.deepcopy(parent.STATE)
            i_child , j_child = Utility.next_pos(parent.i,parent.j,action)
            if state_child[i_child][j_child] == 5: state_child[i_child][j_child] = 0
            visited_positions.add((i_child, j_child))
            child = Node(i_child,j_child,state_child,action,parent)
            if Utility.count_box_cells(state_child) == 0: 
                end = child
                break
            key = (i_child,j_child,tuple(tuple(row) for row in state_child))
            if key not in reached:
                stack.append(child)
                reached.add(key)
        if end is not None: break
    path_states, actions = Utility.trace_path(end)
    return path_states, actions, visited_positions



