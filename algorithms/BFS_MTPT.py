from algorithms import Utility 
import copy 

class Node():
    def __init__(self,i, j, state, action, parent):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
def BFS_MTPT(initial_states):
    import copy
    from algorithms import Utility
    queue = []
    for (i, j, state) in initial_states:
        state = copy.deepcopy(state)
        queue.append(Node(i, j, state, None, None))
    reached = set()
    for x in queue:
        reached.add((x.i, x.j, tuple(tuple(row) for row in x.STATE)))
    end = None
    while queue:
        parent = queue.pop(0)
        moves = Utility.get_actions(parent.i, parent.j, parent.STATE)
        for action in moves:
            state_child = copy.deepcopy(parent.STATE)
            i_child, j_child = Utility.next_pos(parent.i, parent.j, action)
            state_child[i_child][j_child] = 0
            key = (i_child, j_child, tuple(tuple(row) for row in state_child))
            child = Node(i_child, j_child, state_child, action, parent)
            if Utility.count_box_cells(state_child) == 0:
                end = child
                break
            if key not in reached:
                queue.append(child)
                reached.add(key)
        if end is not None:
            break
    return Utility.trace_path(end)