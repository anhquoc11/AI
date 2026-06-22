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

def distance_to_nearest_house(i, j, board):
    min_distance = float('inf')
    for t in range(len(board)):
        for z in range(len(board[0])):
            if board[t][z] == 5:
                distance = abs(i - t) + abs(j - z)
                min_distance = min(min_distance, distance)
    return min_distance if min_distance != float('inf') else 0

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

def is_terminal(state):
    # Trò chơi kết thúc nếu không còn ô '5' (House) trên bản đồ
    return count_box_cells(state) == 0

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