import pygame
import sys
import time
import random
import re
from algorithms import Utility
from algorithms.BFS import BFS
from algorithms.DFS import DFS
from algorithms.greedy import greedy
from algorithms.A_sao import A_sao
from algorithms.Simple_Hill_Climbing import Simple_Hill_Climbing
from algorithms.Local_Beam_Search import Local_Beam_Search

# Configuration
GRID_SIZE = 20
PADDING = 15
FPS = 60

ALG_MAP = {
    'BFS': BFS,
    'DFS': DFS,
    'Greedy': greedy,
    'A*': A_sao,
    'Hill Simple': Simple_Hill_Climbing,
    'Local Beam': Local_Beam_Search,
}

ASSET_PATH = "Assets/"


def load_assets(cell_size):
    def load(name):
        try:
            img = pygame.image.load(ASSET_PATH + name)
            return pygame.transform.scale(img, (cell_size, cell_size))
        except Exception:
            return None

    return {
        'building': load('Building.jpg'),
        'drone': load('Drone.jpg'),
        'house': load('house.jpg'),
        'nofly': load('Nofly.jpg'),
        'tree': load('Tree.png'),
        'warehouse': load('Warehouse.jpg'),
    }


def random_map(size, obstacle_prob=0.12, seed=None):
    """
    Terrain codes:
      0: Tree (free)
      1: No-Fly (impassable)
      2: Building (high cost)
      3: Drone (start) - placed exactly once
      4: Warehouse (goal) - placed exactly once
      5: House (customer) - can be multiple
    """
    if seed is not None:
        random.seed(seed)
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            r = random.random()
            if r < obstacle_prob * 0.5:
                grid[i][j] = 2  # building
            elif r < obstacle_prob * 0.8:
                grid[i][j] = 1  # no-fly (impassable)
            else:
                grid[i][j] = 0  # tree / free

    # Collect free cells (0)
    free_cells = [(i, j) for i in range(size) for j in range(size) if grid[i][j] == 0]
    
    if len(free_cells) < 6:
        # Not enough free cells, retry with lower obstacle prob
        return random_map(size, obstacle_prob=max(0.05, obstacle_prob * 0.8), seed=seed)
    
    # Shuffle and place: drone, warehouse, houses
    random.shuffle(free_cells)
    
    # place exactly one drone (3)
    dx, dy = free_cells[0]
    grid[dx][dy] = 3
    drone_pos = (dx, dy)

    # place exactly one warehouse (goal) (4)
    wx, wy = free_cells[1]
    grid[wx][wy] = 4
    warehouse_pos = (wx, wy)

    # place at least 2-3 houses (5)
    hcount = min(3, len(free_cells) - 2)
    for idx in range(2, 2 + hcount):
        hx, hy = free_cells[idx]
        grid[hx][hy] = 5

    return grid


def choose_algorithm(name):
    n = name.strip().lower()
    mapping = {
        "bfs": "BFS",
        "dfs": "DFS",
        "greedy": "Greedy",
        "astar": "A*",
        "a*": "A*",
        "hill simple": "Hill Simple",
        "local beam": "Local Beam",
    }
    key = mapping.get(n, None)
    if key is None:
        for k in ALG_MAP.keys():
            if k.lower() == name.lower():
                key = k
                break
    if key is None:
        raise ValueError(f"Unknown algorithm: {name}")
    return ALG_MAP[key]


def ui_to_algo_grid(grid, targets):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    algo_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                # no-fly is obstacle
                algo_grid[i][j] = 1
            else:
                # building and other cells are traversable
                algo_grid[i][j] = 0
    for tx, ty in targets:
        if 0 <= tx < rows and 0 <= ty < cols:
            algo_grid[tx][ty] = 5
    return algo_grid


def logs_to_visited(logs):
    coords = set()
    for line in logs:
        for match in re.findall(r"\((\d+),(\d+)\)", line):
            x, y = int(match[0]), int(match[1])
            coords.add((x, y))
    return coords


def compute_path_to_target(start, target, grid, algo):
    temp_grid = [list(row) for row in grid]
    # Clear existing goal markers (warehouse or any temporary target markers)
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            if temp_grid[i][j] == 4:
                temp_grid[i][j] = 0

    # Support a single target or multiple targets
    if isinstance(target, tuple):
        targets = [target]
    else:
        targets = list(target)

    search_grid = ui_to_algo_grid(grid, targets)
    t0 = time.time()
    try:
        result_states, actions, visited_positions = algo(search_grid, start[0], start[1])
    except Exception as e:
        print(f"Error solving path: {e}")
        return [], 0, set(), int((time.time() - t0) * 1000)

    t1 = time.time()
    runtime_ms = int((t1 - t0) * 1000)

    if actions is None:
        return [], 0, visited_positions, runtime_ms

    positions = [start]
    visited = set(visited_positions)
    cost = 0
    current = start
    for a in actions:
        next_pos = Utility.next_pos(current[0], current[1], a)
        positions.append(next_pos)
        visited.add(next_pos)
        current = next_pos
        cost += 1

    return positions, cost, visited, runtime_ms


def main():
    pygame.init()
    
    # Get screen info for fullscreen
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    
    # Calculate layout: left panel + grid
    LEFT_PANEL = max(250, int(screen_width * 0.2))  # 20% for panel, min 250px
    GRID_WIDTH = screen_width - LEFT_PANEL - 3 * PADDING
    GRID_HEIGHT = screen_height - 2 * PADDING
    
    # Cell size based on available grid space
    CELL_SIZE = min(GRID_WIDTH // GRID_SIZE, GRID_HEIGHT // GRID_SIZE)
    
    # Create fullscreen window
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Drone Delivery Pathfinding Simulator")
    clock = pygame.time.Clock()
    assets = load_assets(CELL_SIZE)

    CUSTOM_FONT_SIZE = 16 
    CUSTOM_BIG_FONT_SIZE = 24
    
    font_size = CUSTOM_FONT_SIZE
    big_font_size = CUSTOM_BIG_FONT_SIZE
    try:
        font = pygame.font.Font('./Assets/fonts/font.ttf', font_size)
        bigfont = pygame.font.Font('./Assets/fonts/font.ttf', big_font_size)
    except:
        print("Không tìm thấy file font, đang dùng font mặc định...")
        font = pygame.font.SysFont(None, font_size)
        bigfont = pygame.font.SysFont(None, big_font_size)

    grid = random_map(GRID_SIZE, obstacle_prob=0.12)
    # find drone (3) and warehouse (4)
    start = None
    goal = None
    houses = []  # Initialize houses early
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 3:
                start = (i, j)
            elif grid[i][j] == 4:
                goal = (i, j)
            elif grid[i][j] == 5:
                houses.append((i, j))
    
    if start is None:
        start = (0, 0)
        grid[start[0]][start[1]] = 3
    if goal is None:
        goal = (GRID_SIZE-1, GRID_SIZE-1)
        grid[goal[0]][goal[1]] = 4

    base = start
    selected_algo_name = 'A*'
    algo = choose_algorithm(selected_algo_name)

    path = []
    visited = set()
    total_cost = 0
    runtime_ms = 0

    running = True
    anim_index = 0
    anim_time = 0
    
    # Dropdown state
    algo_options = list(ALG_MAP.keys())  # Get all algorithms
    dropdown_open = False
    dropdown_rect = None
    options_rects = []
    dropdown_scroll_offset = 0
    max_visible_items = 5
    
    # Delivery state machine
    delivery_state = "IDLE"  # IDLE, PICKING, DELIVERING, RETURNING
    current_target = None  # (x, y) of current target
    delivery_log = []
    state_change_time = 0
    delivered_count = 0
    delivered_houses = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if dropdown_rect and dropdown_rect.collidepoint(event.pos):
                        dropdown_open = not dropdown_open
                        dropdown_scroll_offset = 0  # Reset scroll when opening
                    elif dropdown_open:
                        for i, opt_rect in enumerate(options_rects):
                            if opt_rect.collidepoint(event.pos):
                                selected_algo_name = algo_options[dropdown_scroll_offset + i]
                                algo = choose_algorithm(selected_algo_name)
                                dropdown_open = False
                                break
                elif event.button == 4:  # Mouse wheel up
                    if dropdown_open:
                        dropdown_scroll_offset = max(0, dropdown_scroll_offset - 1)
                elif event.button == 5:  # Mouse wheel down
                    if dropdown_open:
                        max_scroll = max(0, len(algo_options) - max_visible_items)
                        dropdown_scroll_offset = min(max_scroll, dropdown_scroll_offset + 1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    grid = random_map(GRID_SIZE, obstacle_prob=0.12)
                    # find new start and goal
                    start = None
                    goal = None
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            if grid[i][j] == 3:
                                start = (i, j)
                            elif grid[i][j] == 4:
                                goal = (i, j)
                    if start is None:
                        start = (0,0)
                        grid[start[0]][start[1]] = 3
                    if goal is None:
                        goal = (GRID_SIZE-1, GRID_SIZE-1)
                        grid[goal[0]][goal[1]] = 4
                    base = start
                    delivered_houses = []
                    path = []
                    visited = set()
                    delivery_state = "IDLE"
                    delivery_log = []
                    delivered_count = 0
                    dropdown_open = False
                    dropdown_scroll_offset = 0
                    # Re-collect houses
                    houses = []
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            if grid[i][j] == 5:
                                houses.append((i, j))
                elif event.key == pygame.K_SPACE:
                    # Start delivery
                    if delivery_state == "IDLE":
                        start = base
                        delivery_state = "PICKING"
                        delivery_log = [f"[PICKING] Flying to Warehouse at ({goal[0]}, {goal[1]})"]
                        delivered_count = 0
                        delivered_houses = []
                        current_target = goal  # warehouse position
                    
                    algo = choose_algorithm(selected_algo_name)
                    path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                    if not path:
                        delivery_log.append(f"[ERROR] {selected_algo_name}: Cannot find path to target!")
                        delivery_state = "IDLE"
                    anim_index = 0
                    anim_time = pygame.time.get_ticks()
                    state_change_time = pygame.time.get_ticks()



        screen.fill((30, 30, 30))
        
        # Handle delivery state transitions
        now = pygame.time.get_ticks()
        if path and delivery_state != "IDLE":
            step = (now - anim_time) // 150
            step = min(step, len(path) - 1)

            # Mark houses delivered as the drone reaches them on the current path
            if delivery_state == "DELIVERING":
                dx, dy = path[step]
                if (dx, dy) in houses and (dx, dy) not in delivered_houses:
                    delivered_count += 1
                    delivered_houses.append((dx, dy))
                    houses = [h for h in houses if h != (dx, dy)]
                    grid[dx][dy] = 0
                    delivery_log.append(f"[DELIVERED] House #{delivered_count} at ({dx}, {dy})")

            # Check if animation finished
            if (now - anim_time) // 150 >= len(path):
                # Drone reached goal
                if delivery_state == "PICKING":
                    delivery_log.append(f"[PICKED UP] At Warehouse. Now delivering all houses...")
                    if houses:
                        delivery_state = "DELIVERING"
                        current_target = houses
                        delivery_log.append(f"[DELIVERING] Planning route for {len(houses)} houses...")
                        state_change_time = now
                    else:
                        delivery_state = "IDLE"
                        delivery_log.append("[DONE] No houses to deliver")

                elif delivery_state == "DELIVERING":
                    delivery_state = "RETURNING"
                    current_target = base
                    delivery_log.append(f"[RETURNING] All delivered! Flying back to Base at ({base[0]}, {base[1]})")
                    state_change_time = now

                elif delivery_state == "RETURNING":
                    # Returned to base, mission complete
                    delivery_state = "IDLE"
                    delivery_log.append("[DONE] Mission Complete! All packages delivered and returned.")

                # Update current drone position after arriving at the target
                start = path[-1]

                # Immediately plan the next leg when not idle
                if delivery_state != "IDLE":
                    algo = choose_algorithm(selected_algo_name)
                    path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                    if not path:
                        delivery_log.append(f"[ERROR] {selected_algo_name}: Cannot find path to target!")
                        delivery_state = "IDLE"
                    anim_time = now
                    state_change_time = now

        # Draw left panel
        panel_x = PADDING
        panel_y = PADDING
        pygame.draw.rect(screen, (40, 40, 40), (panel_x, panel_y, LEFT_PANEL - PADDING, GRID_SIZE * CELL_SIZE))

        screen.blit(bigfont.render('THUẬT TOÁN', True, (200, 200, 200)), (panel_x + 10, panel_y + 10))
        
        # Draw algorithm dropdown
        dropdown_y = panel_y + 50
        dropdown_height = font_size + 10
        dropdown_rect = pygame.Rect(panel_x + 10, dropdown_y, LEFT_PANEL - PADDING - 20, dropdown_height)
        pygame.draw.rect(screen, (60, 60, 60), dropdown_rect, 2)
        screen.blit(font.render(selected_algo_name, True, (255, 255, 100)), (panel_x + 15, dropdown_y + 5))
        
        # Draw dropdown arrow
        arrow_x = dropdown_rect.right - 15
        arrow_y = dropdown_rect.centery
        pygame.draw.polygon(screen, (200, 200, 200), [(arrow_x, arrow_y - 3), (arrow_x + 5, arrow_y - 3), (arrow_x + 2.5, arrow_y + 3)])
        
        # Draw options if dropdown is open
        options_rects = []
        if dropdown_open:
            visible_items = algo_options[dropdown_scroll_offset:dropdown_scroll_offset + max_visible_items]
            for i, opt in enumerate(visible_items):
                opt_y = dropdown_y + dropdown_height + i * (font_size + 5)
                opt_rect = pygame.Rect(panel_x + 10, opt_y, LEFT_PANEL - PADDING - 20, font_size + 5)
                opt_color = (100, 100, 150) if opt == selected_algo_name else (70, 70, 70)
                pygame.draw.rect(screen, opt_color, opt_rect)
                pygame.draw.rect(screen, (200, 200, 200), opt_rect, 1)
                opt_text_color = (255, 255, 100) if opt == selected_algo_name else (200, 200, 200)
                screen.blit(font.render(opt[:20], True, opt_text_color), (panel_x + 15, opt_y + 3))  # Truncate long names
                options_rects.append(opt_rect)
            
            # Draw scroll indicator if there are more items
            if len(algo_options) > max_visible_items:
                scroll_text = f"↑↓ {dropdown_scroll_offset+1}/{len(algo_options)}"
                scroll_color = (150, 150, 100)
                screen.blit(font.render(scroll_text, True, scroll_color), (panel_x + 15, dropdown_y + dropdown_height + max_visible_items * (font_size + 5) + 3))
        
        # controls
        ctrl_y = panel_y + 220
        screen.blit(font.render('[SPACE] START', True, (200,200,200)), (panel_x + 10, ctrl_y))
        screen.blit(font.render('[R] RANDOM', True, (200,200,200)), (panel_x + 10, ctrl_y + font_size + 5))
        screen.blit(font.render('[ESC] EXIT', True, (200,200,200)), (panel_x + 10, ctrl_y + 2*(font_size + 5)))

        # Draw grid
        grid_x0 = LEFT_PANEL + PADDING
        grid_y0 = PADDING
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = grid[i][j]
                rect = pygame.Rect(grid_x0 + j*CELL_SIZE, grid_y0 + i*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
                color = (240, 240, 240)
                if cell == 2:
                    color = (160, 160, 160)  # building
                elif cell == 1:
                    color = (120, 30, 30)    # no-fly
                elif cell == 4:
                    color = (255, 220, 100)  # warehouse (goal)
                elif cell == 5:
                    color = (220, 140, 80)   # house (customer)
                elif cell == 3:
                    color = (240, 240, 240)  # drone base
                elif cell == 0:
                    color = (180, 225, 180)  # tree
                pygame.draw.rect(screen, color, rect)

        # draw visited
        for (x, y) in visited:
            rect = pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            pygame.draw.rect(screen, (100, 200, 150), rect)

        # draw final path
        for (x, y) in path:
            rect = pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            pygame.draw.rect(screen, (230, 220, 100), rect)

        # draw delivered houses overlay
        for (x, y) in delivered_houses:
            rect = pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            pygame.draw.rect(screen, (120, 180, 255), rect)
            pygame.draw.circle(screen, (0, 80, 200), (grid_x0 + y*CELL_SIZE + CELL_SIZE//2, grid_y0 + x*CELL_SIZE + CELL_SIZE//2), max(2, CELL_SIZE//4))

        # highlight current delivery target(s)
        if current_target is not None and delivery_state in ("DELIVERING", "PICKING", "RETURNING"):
            if isinstance(current_target, list):
                for tx, ty in current_target:
                    rect = pygame.Rect(grid_x0 + ty*CELL_SIZE, grid_y0 + tx*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
                    pygame.draw.rect(screen, (255, 140, 0), rect, 2)
            else:
                tx, ty = current_target
                rect = pygame.Rect(grid_x0 + ty*CELL_SIZE, grid_y0 + tx*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
                pygame.draw.rect(screen, (255, 140, 0), rect, 3)

        # draw warehouse(s), house and buildings/nofly/tree icons where applicable
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = grid[i][j]
                x = grid_x0 + j*CELL_SIZE
                y = grid_y0 + i*CELL_SIZE
                if cell == 4 and assets.get('warehouse'):
                    screen.blit(assets['warehouse'], (x, y))
                elif cell == 5 and assets.get('house'):
                    screen.blit(assets['house'], (x, y))
                elif cell == 2 and assets.get('building'):
                    screen.blit(assets['building'], (x, y))
                elif cell == 1 and assets.get('nofly'):
                    screen.blit(assets['nofly'], (x, y))
                elif cell == 0 and assets.get('tree'):
                    screen.blit(assets['tree'], (x, y))

        # draw drone (animated along path) or at start if no path
        if path:
            now = pygame.time.get_ticks()
            # one step per 150ms
            step = (now - anim_time) // 150
            # Clamp step to not exceed path length
            step = min(step, len(path) - 1)
            dx, dy = path[step]
            if assets.get('drone'):
                screen.blit(assets['drone'], (grid_x0 + dy*CELL_SIZE, grid_y0 + dx*CELL_SIZE))
            else:
                pygame.draw.circle(screen, (255, 0, 0), (grid_x0 + dy*CELL_SIZE + CELL_SIZE//2, grid_y0 + dx*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)
        else:
            # draw drone at start if no path yet
            sx, sy = start
            if assets.get('drone'):
                screen.blit(assets['drone'], (grid_x0 + sy*CELL_SIZE, grid_y0 + sx*CELL_SIZE))
            else:
                pygame.draw.circle(screen, (255, 0, 0), (grid_x0 + sy*CELL_SIZE + CELL_SIZE//2, grid_y0 + sx*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)

        # Draw legend and statistics on left panel
        stats_y = panel_y + 330
        screen.blit(bigfont.render('THỐNG KÊ', True, (200,200,200)), (panel_x + 10, stats_y))
        screen.blit(font.render(f"Nodes Visited : {len(visited)}", True, (200,200,200)), (panel_x + 12, stats_y + 36))
        screen.blit(font.render(f"Path Length   : {max(0, len(path)-1)}", True, (200,200,200)), (panel_x + 12, stats_y + 56))
        screen.blit(font.render(f"Total Cost    : {total_cost}", True, (200,200,200)), (panel_x + 12, stats_y + 76))
        screen.blit(font.render(f"Delivered     : {len(delivered_houses)}", True, (200,200,200)), (panel_x + 12, stats_y + 96))
        screen.blit(font.render(f"Runtime       : {runtime_ms} ms", True, (200,200,200)), (panel_x + 12, stats_y + 116))
        
        # Draw delivery log
        log_y = stats_y + 160
        screen.blit(bigfont.render('LOG', True, (200,200,200)), (panel_x + 10, log_y))
        for i, log_line in enumerate(delivery_log[-5:]):  # Show last 5 lines
            log_color = (100, 200, 150) if "DELIVERED" in log_line else (200, 150, 100) if "PICKING" in log_line else (200, 200, 200)
            screen.blit(font.render(log_line[:30], True, log_color), (panel_x + 12, log_y + 36 + i*(font_size + 3)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()