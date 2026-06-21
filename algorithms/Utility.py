import copy

def get_actions(i, j, board):
    result = []
    if i > 0 and board[i-1][j] != 1: result.append("UP")
    if i < len(board) - 1 and board[i+1][j] != 1: result.append("DOWN")
    if j > 0 and board[i][j-1] != 1: result.append("LEFT")
    if j < len(board[0]) - 1 and board[i][j+1] != 1: result.append("RIGHT")
    return result

def next_pos(i,j,action):
    if action == "UP": return i-1,j
    if action == "DOWN": return i+1,j
    if action == "RIGHT": return i,j+1
    if action == "LEFT": return i,j-1

def count_box_cells(board):
    cost = 0
    for t in range(len(board)):
        for z in range(len(board[0])):
            if board[t][z] == 5: cost += 1
    return cost

def queue_priority_add(queue, x):
    for index in range(len(queue)):
        if x.F <= queue[index].F: 
            queue.insert(index,x)
            return queue
    queue.append(x)
    return queue

def queue_priority_add_UCS(queue, x):
    for index in range(len(queue)):
        if x.G <= queue[index].G: 
            queue.insert(index,x)
            return queue
    queue.append(x)
    return queue

def queue_priority_add_greedy(queue, x):
    for index in range(len(queue)):
        if x.H <= queue[index].H: 
            queue.insert(index,x)
            return queue
    queue.append(x)
    return queue

def trace_path(end):
    path_states = []
    actions = []
    node = end
    while node is not None:
        path_states.append(node.STATE)
        if node.ACTION is not None:
            actions.append(node.ACTION)
        node = node.PARENT
    path_states.reverse()
    actions.reverse()
    return path_states, actions