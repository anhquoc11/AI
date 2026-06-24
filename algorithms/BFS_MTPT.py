from algorithms import Utility
import copy


class Node():
    def __init__(self, i, j, state, action, parent):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent


def BFS_MTPT(initial_states):
    queue = []
    reached = set()
    visited_positions = set()
    for (grid,start_i, start_j) in initial_states:
        start_state = copy.deepcopy(grid)
        start_state[start_i][start_j] = 0
        node = Node(start_i, start_j, start_state, None, None)
        queue.append(node)
        key = (start_i, start_j, tuple(tuple(row) for row in start_state))
        reached.add(key)
        visited_positions.add((start_i, start_j))
        if Utility.count_box_cells(start_state) == 0:
            return [start_state], [], visited_positions
    end = None
    while queue:
        parent = queue.pop(0)
        moves = Utility.get_actions(parent.i, parent.j, parent.STATE)
        for action in moves:
            i_child, j_child = Utility.next_pos(parent.i, parent.j, action)
            state_child = copy.deepcopy(parent.STATE)
            state_child[i_child][j_child] = 0
            visited_positions.add((i_child, j_child))
            if Utility.count_box_cells(state_child) == 0:
                end = Node(i_child, j_child, state_child, action, parent)
                queue.clear()
                break
            key = (i_child, j_child, tuple(tuple(row) for row in state_child))
            if key not in reached:
                child = Node(i_child, j_child, state_child, action, parent)
                queue.append(child)
                reached.add(key)
        if end is not None:
            break
    if end is None:
        return [], [], visited_positions
    path_states, actions = Utility.trace_path(end)
    return path_states, actions, visited_positions