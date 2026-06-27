import pygame 

def draw_cells(screen, grid, GRID_SIZE, CELL_SIZE, grid_x0, grid_y0):

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell = grid[i][j]
            rect = pygame.Rect(grid_x0 + j*CELL_SIZE, grid_y0 + i*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            color = (240, 240, 240)
            if cell == 2: color = (160, 160, 160)
            elif cell == 1: color = (120, 30, 30)
            elif cell == 4: color = (255, 220, 100)
            elif cell == 5: color = (220, 140, 80)
            elif cell == 3: color = (240, 240, 240)
            elif cell == 0: color = (180, 225, 180)
            pygame.draw.rect(screen, color, rect)

def draw_visited(visited,screen,grid_x0,grid_y0,CELL_SIZE):
    for (x, y) in visited:
        pygame.draw.rect(screen, (100, 200, 150), pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

def draw_path(path,screen,grid_x0,grid_y0,CELL_SIZE):
    for (x, y) in path:
           pygame.draw.rect(screen, (230, 220, 100), pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

def draw_delivered(delivered_houses,screen,grid_x0,grid_y0,CELL_SIZE):
    for (x, y) in delivered_houses:
        pygame.draw.rect(screen, (120, 180, 255), pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
        pygame.draw.circle(screen, (0, 80, 200), (grid_x0 + y*CELL_SIZE + CELL_SIZE//2, grid_y0 + x*CELL_SIZE + CELL_SIZE//2), max(2, CELL_SIZE//4))

def draw_targets(screen,current_target,delivery_state,CELL_SIZE,grid_x0,grid_y0):
    if current_target is not None and delivery_state in ("DELIVERING", "PICKING", "RETURNING"):
        if isinstance(current_target, list):
            for tx, ty in current_target:
                pygame.draw.rect(screen, (255, 140, 0), pygame.Rect(grid_x0 + ty*CELL_SIZE, grid_y0 + tx*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1), 2)
        else:
            tx, ty = current_target
            pygame.draw.rect(screen, (255, 140, 0), pygame.Rect(grid_x0 + ty*CELL_SIZE, grid_y0 + tx*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1), 3)

def draw_objects(assets,GRID_SIZE,grid,grid_x0,grid_y0,CELL_SIZE,screen):
    for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = grid[i][j]
                x = grid_x0 + j*CELL_SIZE
                y = grid_y0 + i*CELL_SIZE
                if cell == 4 and assets.get('warehouse'): screen.blit(assets['warehouse'], (x, y))
                elif cell == 5 and assets.get('house'): screen.blit(assets['house'], (x, y))
                elif cell == 2 and assets.get('building'): screen.blit(assets['building'], (x, y))
                elif cell == 1 and assets.get('nofly'): screen.blit(assets['nofly'], (x, y))
                elif cell == 0 and assets.get('tree'): screen.blit(assets['tree'], (x, y))

def draw_drone(assets,path,current_step ,grid_x0,grid_y0,CELL_SIZE,screen,start):
    if path and current_step < len(path):
        dx, dy = path[current_step]
        if assets.get('drone'): screen.blit(assets['drone'], (grid_x0 + dy*CELL_SIZE, grid_y0 + dx*CELL_SIZE))
        else: pygame.draw.circle(screen, (255, 0, 0), (grid_x0 + dy*CELL_SIZE + CELL_SIZE//2, grid_y0 + dx*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)
    else:
        sx, sy = start
        if assets.get('drone'): screen.blit(assets['drone'], (grid_x0 + sy*CELL_SIZE, grid_y0 + sx*CELL_SIZE))
        else: pygame.draw.circle(screen, (255, 0, 0), (grid_x0 + sy*CELL_SIZE + CELL_SIZE//2, grid_y0 + sx*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)
