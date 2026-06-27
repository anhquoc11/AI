import random

def random_map(size, obstacle_prob=0.12, seed=None):
    if seed is not None: random.seed(seed)
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            r = random.random()
            if r < obstacle_prob * 0.5: grid[i][j] = 2
            elif r < obstacle_prob * 0.8: grid[i][j] = 1
            else: grid[i][j] = 0
    free_cells = [(i, j) for i in range(size) for j in range(size) if grid[i][j] == 0]
    if len(free_cells) < 6: return random_map(size, obstacle_prob=max(0.05, obstacle_prob * 0.8), seed=seed)
    random.shuffle(free_cells)
    dx, dy = free_cells[0]
    grid[dx][dy] = 3
    wx, wy = free_cells[1]
    grid[wx][wy] = 4
    hcount = min(4, len(free_cells) - 2)
    for idx in range(2, 2 + hcount):
        hx, hy = free_cells[idx]
        grid[hx][hy] = 5
    return grid
