import time 
from algorithms import Utility
from algorithms.and_or_search import and_or_search

def movement_cost(cell_value):
    return 5 if cell_value == 2 else 1

# chuẩn hóa ma trận phù hợp với target
def ui_to_algo_grid(grid, targets):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    algo_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                algo_grid[i][j] = 1
            elif grid[i][j] == 2:
                algo_grid[i][j] = 2
            else:
                algo_grid[i][j] = 0
    for tx, ty in targets:
        if 0 <= tx < rows and 0 <= ty < cols:
            algo_grid[tx][ty] = 5
    return algo_grid

# gọi thuật toán theo lựa chọn
def compute_path_to_target(start, target, grid, algo):
    targets = [target] if isinstance(target, tuple) else list(target)
    search_grid = ui_to_algo_grid(grid, targets)
    t0 = time.time()
    try:
        result_states, actions, visited_positions = algo(search_grid, start[0], start[1])
    except Exception as e:
        return [], 0, set(), int((time.time() - t0) * 1000)
    t1 = time.time()
    runtime_ms = int((t1 - t0) * 1000)
    if actions is None: return [], 0, visited_positions, runtime_ms
    positions = [start]
    visited = set(visited_positions)
    cost = 0
    current = start
    for a in actions:
        next_pos = Utility.next_pos(current[0], current[1], a)
        positions.append(next_pos)
        visited.add(next_pos)
        current = next_pos
        cost += movement_cost(grid[current[0]][current[1]])
    return positions, cost, visited, runtime_ms

# xem xét việc lựa chọn đơn hàng sao cho không hết nhiên liệu giữa đường
def find_safe_orders(selected_orders, fuel, grid, start, algo):
    history = []
    for k in range(len(selected_orders), 0, -1):
        candidate = selected_orders[:k]
        houses = [o['pos'] for o in candidate]
        path, total_cost, visited, runtime_ms = compute_path_to_target(start,houses,grid,algo)
        safe = and_or_search(fuel,total_cost,len(houses))
        history.append((k, safe))
        if safe:
            return candidate, total_cost, history
    return [], 0, history
