import random
from core.map_generator import random_map

def create_map(GRID_SIZE):
    grid = random_map(GRID_SIZE, obstacle_prob=0.12)

    start = None
    goal = None
    warehouse_orders = []

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 3:
                start = (i, j)
            elif grid[i][j] == 4:
                goal = (i, j)

            elif grid[i][j] == 5:
                grid[i][j] = 0
                warehouse_orders.append({
                    'w': random.randint(3, 7),
                    'v': random.randint(10, 50),
                    'pos': (i, j)
                })

    if start is None:
        start = (0, 0)
        grid[0][0] = 3

    if goal is None:
        goal = (GRID_SIZE - 1, GRID_SIZE - 1)
        grid[goal[0]][goal[1]] = 4

    return grid, start, goal, warehouse_orders