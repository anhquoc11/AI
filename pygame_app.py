import pygame
import sys
import time
import random
import re
import copy
from algorithms import Utility
from algorithms.BFS import BFS
from algorithms.DFS import DFS
from algorithms.greedy import greedy
from algorithms.A_sao import A_sao
from algorithms.Simple_Hill_Climbing import Simple_Hill_Climbing
from algorithms.Local_Beam_Search import Local_Beam_Search

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

# ==================== LOGIC CARO (TẠI KHO) ====================
class CaroNode:
    def __init__(self, state, action, parent):
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent

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

def alpha_beta_caro(node, depth, alpha, beta, is_maximizing):
    if depth == 0 or is_terminal_caro(node.STATE):
        return evaluate_caro(node.STATE), None
    best_action = None
    if is_maximizing:
        max_eval = float('-inf')
        for action in get_actions_caro(node.STATE):
            new_state = copy.deepcopy(node.STATE)
            new_state[action[0]][action[1]] = 2
            eval, _ = alpha_beta_caro(CaroNode(new_state, action, node), depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_action = action
            alpha = max(alpha, eval)
            if beta <= alpha: break
        return max_eval, best_action
    else:
        min_eval = float('inf')
        for action in get_actions_caro(node.STATE):
            new_state = copy.deepcopy(node.STATE)
            new_state[action[0]][action[1]] = 1
            eval, _ = alpha_beta_caro(CaroNode(new_state, action, node), depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_action = action
            beta = min(beta, eval)
            if beta <= alpha: break
        return min_eval, best_action


# ==================== LOGIC XẾP HÀNG (TẠI NHÀ GIAO) ====================
C4_ROWS = 5
C4_COLS = 6
EMPTY = 0
PLAYER_C4 = 1
AI_C4 = 2

class DropNode:
    def __init__(self, state, action, parent):
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent

def get_valid_columns(state):
    return [c for c in range(C4_COLS) if state[0][c] == EMPTY]

def get_next_open_row(state, col):
    for r in range(C4_ROWS-1, -1, -1):
        if state[r][col] == EMPTY:
            return r
    return -1

def winning_move_c4(state, piece):
    for c in range(C4_COLS - 3):
        for r in range(C4_ROWS):
            if state[r][c] == piece and state[r][c+1] == piece and state[r][c+2] == piece and state[r][c+3] == piece: return True
    for c in range(C4_COLS):
        for r in range(C4_ROWS - 3):
            if state[r][c] == piece and state[r+1][c] == piece and state[r+2][c] == piece and state[r+3][c] == piece: return True
    for c in range(C4_COLS - 3):
        for r in range(C4_ROWS - 3):
            if state[r][c] == piece and state[r+1][c+1] == piece and state[r+2][c+2] == piece and state[r+3][c+3] == piece: return True
    for c in range(C4_COLS - 3):
        for r in range(3, C4_ROWS):
            if state[r][c] == piece and state[r-1][c+1] == piece and state[r-2][c+2] == piece and state[r-3][c+3] == piece: return True
    return False

def is_terminal_c4(state):
    return winning_move_c4(state, PLAYER_C4) or winning_move_c4(state, AI_C4) or len(get_valid_columns(state)) == 0

def evaluate_c4(state):
    if winning_move_c4(state, AI_C4): return 100
    if winning_move_c4(state, PLAYER_C4): return -100
    return 0

def minimax_drop(node, depth, is_maximizing):
    if depth == 0 or is_terminal_c4(node.STATE):
        if depth == 0 and not is_terminal_c4(node.STATE): return 0, None
        return evaluate_c4(node.STATE), None
    valid_columns = get_valid_columns(node.STATE)
    best_action = random.choice(valid_columns) if valid_columns else None

    if is_maximizing:
        max_eval = float('-inf')
        for col in valid_columns:
            row = get_next_open_row(node.STATE, col)
            new_state = copy.deepcopy(node.STATE)
            new_state[row][col] = AI_C4
            child = DropNode(new_state, col, node)
            eval, _ = minimax_drop(child, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_action = col
        return max_eval, best_action
    else:
        min_eval = float('inf')
        for col in valid_columns:
            row = get_next_open_row(node.STATE, col)
            new_state = copy.deepcopy(node.STATE)
            new_state[row][col] = PLAYER_C4
            child = DropNode(new_state, col, node)
            eval, _ = minimax_drop(child, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_action = col
        return min_eval, best_action

# ==================== MAIN GAME ====================

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
    hcount = min(3, len(free_cells) - 2)
    for idx in range(2, 2 + hcount):
        hx, hy = free_cells[idx]
        grid[hx][hy] = 5
    return grid

def choose_algorithm(name):
    n = name.strip().lower()
    mapping = {
        "bfs": "BFS", "dfs": "DFS", "greedy": "Greedy",
        "astar": "A*", "a*": "A*", "hill simple": "Hill Simple",
        "local beam": "Local Beam",
    }
    key = mapping.get(n, None)
    if key is None:
        for k in ALG_MAP.keys():
            if k.lower() == name.lower():
                key = k
                break
    if key is None: raise ValueError(f"Unknown algorithm: {name}")
    return ALG_MAP[key]

def ui_to_algo_grid(grid, targets):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    algo_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1: algo_grid[i][j] = 1
            else: algo_grid[i][j] = 0
    for tx, ty in targets:
        if 0 <= tx < rows and 0 <= ty < cols:
            algo_grid[tx][ty] = 5
    return algo_grid

def compute_path_to_target(start, target, grid, algo):
    temp_grid = [list(row) for row in grid]
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            if temp_grid[i][j] == 4: temp_grid[i][j] = 0
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
        cost += 1
    return positions, cost, visited, runtime_ms

def main():
    pygame.init()
    
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Drone Delivery & AI Minigames")
    clock = pygame.time.Clock()
    
    # === SỬA LỖI GIAO DIỆN Ở ĐÂY: TĂNG LEFT_PANEL TỪ 250 -> 380 ===
    LEFT_PANEL = max(380, int(screen_width * 0.28))
    GRID_WIDTH = screen_width - LEFT_PANEL - 3 * PADDING
    GRID_HEIGHT = screen_height - 2 * PADDING
    CELL_SIZE = min(GRID_WIDTH // GRID_SIZE, GRID_HEIGHT // GRID_SIZE)
    assets = load_assets(CELL_SIZE)
    
    CUSTOM_FONT_SIZE = 16 
    CUSTOM_BIG_FONT_SIZE = 24
    font_size = CUSTOM_FONT_SIZE
    big_font_size = CUSTOM_BIG_FONT_SIZE
    try:
        font = pygame.font.Font('./Assets/fonts/font.ttf', font_size)
        bigfont = pygame.font.Font('./Assets/fonts/font.ttf', big_font_size)
    except:
        font = pygame.font.SysFont(None, font_size)
        bigfont = pygame.font.SysFont(None, big_font_size)
        
    grid = random_map(GRID_SIZE, obstacle_prob=0.12)
    start = None
    goal = None
    houses = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 3: start = (i, j)
            elif grid[i][j] == 4: goal = (i, j)
            elif grid[i][j] == 5: houses.append((i, j))
            
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
    
    algo_options = list(ALG_MAP.keys())
    dropdown_open = False
    dropdown_rect = None
    options_rects = []
    dropdown_scroll_offset = 0
    max_visible_items = 5
    delivery_state = "IDLE"
    current_target = None
    
    # === THÔNG SỐ LOG ===
    delivery_log = []
    log_scroll_offset = 0
    max_visible_logs = 6
    prev_log_length = 0
    log_rect = pygame.Rect(0, 0, 0, 0) # Khởi tạo tạm
    
    delivered_count = 0
    delivered_houses = []
    
    # State: Caro
    caro_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    in_minigame_caro = False
    caro_player_turn = True
    caro_rects = [[None for _ in range(3)] for _ in range(3)]
    
    # State: Connect 4
    connect4_board = [[EMPTY for _ in range(C4_COLS)] for _ in range(C4_ROWS)]
    in_connect4 = False
    c4_player_turn = True
    current_house = None
    
    DIFFICULTY_LEVELS = ["DỄ", "TRUNG BÌNH", "KHÓ"]
    current_difficulty_idx = 2 
    
    fuel = 60
    current_step = 0
    move_timer = 0
    ai_timer = 0 # Thêm biến đếm thời gian cho AI

    while running:
        now = pygame.time.get_ticks()
        diff_rect = pygame.Rect(PADDING + 10, PADDING + 130, LEFT_PANEL - PADDING - 20, font_size + 10)
        
        # Calculate Connect 4 UI boundaries
        c4_board_width = 420
        c4_board_height = 350
        c4_start_x = screen_width // 2 - c4_board_width // 2
        c4_start_y = screen_height // 2 - c4_board_height // 2
        c4_cell_s = c4_board_width // C4_COLS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                
                # === SỬA LỖI GIAO DIỆN Ở ĐÂY: TĂNG LEFT_PANEL KHI RESIZE ===
                LEFT_PANEL = max(380, int(screen_width * 0.28))
                GRID_WIDTH = screen_width - LEFT_PANEL - 3 * PADDING
                GRID_HEIGHT = screen_height - 2 * PADDING
                CELL_SIZE = min(GRID_WIDTH // GRID_SIZE, GRID_HEIGHT // GRID_SIZE)
                assets = load_assets(CELL_SIZE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Đổi độ khó AI
                    if not in_minigame_caro and not in_connect4 and diff_rect.collidepoint(event.pos):
                        current_difficulty_idx = (current_difficulty_idx + 1) % len(DIFFICULTY_LEVELS)
                    
                    # Tương tác với Cờ Caro
                    elif in_minigame_caro and caro_player_turn:
                        mx, my = event.pos
                        for r in range(3):
                            for c in range(3):
                                if caro_rects[r][c] and caro_rects[r][c].collidepoint((mx, my)) and caro_board[r][c] == 0:
                                    caro_board[r][c] = 1
                                    caro_player_turn = False
                                    ai_timer = pygame.time.get_ticks() # Lưu mốc thời gian click
                    
                    # Tương tác với Connect 4
                    elif in_connect4 and c4_player_turn:
                        mx, my = event.pos
                        if c4_start_x <= mx <= c4_start_x + c4_board_width and c4_start_y <= my <= c4_start_y + c4_board_height:
                            col = (mx - c4_start_x) // c4_cell_s
                            row = get_next_open_row(connect4_board, col)
                            if row != -1:
                                connect4_board[row][col] = PLAYER_C4
                                c4_player_turn = False
                                ai_timer = pygame.time.get_ticks() # Lưu mốc thời gian click

                    # Tương tác với Menu
                    else:
                        if dropdown_rect and dropdown_rect.collidepoint(event.pos):
                            dropdown_open = not dropdown_open
                            dropdown_scroll_offset = 0
                        elif dropdown_open:
                            for i, opt_rect in enumerate(options_rects):
                                if opt_rect.collidepoint(event.pos):
                                    selected_algo_name = algo_options[dropdown_scroll_offset + i]
                                    algo = choose_algorithm(selected_algo_name)
                                    dropdown_open = False
                                    break
                
                # Logic Lăn chuột (Scroll)
                elif event.button == 4: # Scroll Up
                    if dropdown_open:
                        dropdown_scroll_offset = max(0, dropdown_scroll_offset - 1)
                    elif log_rect.collidepoint(event.pos):
                        log_scroll_offset = max(0, log_scroll_offset - 1)
                elif event.button == 5: # Scroll Down
                    if dropdown_open:
                        max_scroll = max(0, len(algo_options) - max_visible_items)
                        dropdown_scroll_offset = min(max_scroll, dropdown_scroll_offset + 1)
                    elif log_rect.collidepoint(event.pos):
                        max_log_scroll = max(0, len(delivery_log) - max_visible_logs)
                        log_scroll_offset = min(max_log_scroll, log_scroll_offset + 1)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    grid = random_map(GRID_SIZE, obstacle_prob=0.12)
                    start = None
                    goal = None
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            if grid[i][j] == 3: start = (i, j)
                            elif grid[i][j] == 4: goal = (i, j)
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
                    log_scroll_offset = 0
                    prev_log_length = 0
                    delivered_count = 0
                    dropdown_open = False
                    dropdown_scroll_offset = 0
                    houses = []
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            if grid[i][j] == 5: houses.append((i, j))
                    in_minigame_caro = False
                    caro_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                    caro_player_turn = True
                    in_connect4 = False
                    connect4_board = [[EMPTY for _ in range(C4_COLS)] for _ in range(C4_ROWS)]
                    c4_player_turn = True
                    fuel = 60
                    current_step = 0
                elif event.key == pygame.K_SPACE:
                    if delivery_state in ("IDLE", "OUT_OF_FUEL") and not in_minigame_caro and not in_connect4:
                        if fuel <= 0: fuel = 60
                        start = base
                        delivery_state = "PICKING"
                        delivery_log.append("Bay tới Kho...")
                        delivered_count = 0
                        delivered_houses = []
                        current_target = goal
                        current_step = 0
                        algo = choose_algorithm(selected_algo_name)
                        path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                        if not path:
                            delivery_state = "IDLE"
                        move_timer = pygame.time.get_ticks()

        # Cập nhật cuộn log tự động nếu có thông báo mới
        if len(delivery_log) != prev_log_length:
            log_scroll_offset = max(0, len(delivery_log) - max_visible_logs)
            prev_log_length = len(delivery_log)

        # ================= AI CARO (TẠI KHO) =================
        # THÊM ĐỘ TRỄ 300ms CHO AI
        if in_minigame_caro and not caro_player_turn and (now - ai_timer > 300):
            opt_prob = 1.0 
            if DIFFICULTY_LEVELS[current_difficulty_idx] == "DỄ": opt_prob = 0.20 
            elif DIFFICULTY_LEVELS[current_difficulty_idx] == "TRUNG BÌNH": opt_prob = 0.70 
            
            if random.random() < opt_prob:
                score, best_move = alpha_beta_caro(CaroNode(caro_board, None, None), 9, float('-inf'), float('inf'), True)
            else:
                available_moves = get_actions_caro(caro_board)
                best_move = random.choice(available_moves) if available_moves else None

            if best_move:
                caro_board[best_move[0]][best_move[1]] = 2
            caro_player_turn = True

        if in_minigame_caro and is_terminal_caro(caro_board):
            pygame.time.delay(1000)
            winner = check_winner_caro(caro_board)
            if winner == 1:
                fuel += 50
                delivery_log.append("Caro Thắng! +50 Nhiên liệu")
            elif winner == 2:
                delivery_log.append("Caro Thua! Không có nhiên liệu")
            else:
                fuel += 20
                delivery_log.append("Caro Hòa! +20 Nhiên liệu")

            in_minigame_caro = False
            caro_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            caro_player_turn = True
            
            if houses:
                delivery_state = "DELIVERING"
                current_target = houses
            else:
                delivery_state = "RETURNING"
                current_target = base

            if delivery_state != "IDLE":
                start = path[-1]
                algo = choose_algorithm(selected_algo_name)
                path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                current_step = 0
                move_timer = pygame.time.get_ticks()

        # ================= AI CONNECT 4 (TẠI NHÀ GIAO) =================
        # THÊM ĐỘ TRỄ 300ms CHO AI
        if in_connect4 and not c4_player_turn and (now - ai_timer > 300):
            opt_prob = 1.0 
            if DIFFICULTY_LEVELS[current_difficulty_idx] == "DỄ": opt_prob = 0.20 
            elif DIFFICULTY_LEVELS[current_difficulty_idx] == "TRUNG BÌNH": opt_prob = 0.70 
            
            if random.random() < opt_prob:
                score, best_col = minimax_drop(DropNode(connect4_board, None, None), 4, True)
            else:
                avail_cols = get_valid_columns(connect4_board)
                best_col = random.choice(avail_cols) if avail_cols else None

            if best_col is not None:
                row = get_next_open_row(connect4_board, best_col)
                connect4_board[row][best_col] = AI_C4
            c4_player_turn = True

        if in_connect4 and is_terminal_c4(connect4_board):
            pygame.time.delay(1000)
            if winning_move_c4(connect4_board, PLAYER_C4):
                fuel += 30
                delivery_log.append("Giao hàng & Xếp Thắng! +30 Nhiên liệu")
            elif winning_move_c4(connect4_board, AI_C4):
                fuel -= 10
                delivery_log.append("Xếp hàng Thua! Phạt -10 Nhiên liệu")
            else:
                fuel += 10
                delivery_log.append("Hòa! +10 Nhiên liệu")

            in_connect4 = False
            connect4_board = [[EMPTY for _ in range(C4_COLS)] for _ in range(C4_ROWS)]
            c4_player_turn = True
            
            # Đã giao xong
            delivered_count += 1
            delivered_houses.append(current_house)
            houses = [h for h in houses if h != current_house]
            grid[current_house[0]][current_house[1]] = 0
            
            move_timer = pygame.time.get_ticks()

        # ================= MOVEMENT DRONE =================
        if path and delivery_state not in ("IDLE", "OUT_OF_FUEL") and not in_minigame_caro and not in_connect4:
            if now - move_timer > 150:
                move_timer = now
                if current_step < len(path) - 1:
                    if fuel > 0:
                        fuel -= 1
                        current_step += 1
                        dx, dy = path[current_step]
                        
                        if delivery_state == "DELIVERING":
                            if (dx, dy) in houses and (dx, dy) not in delivered_houses:
                                in_connect4 = True
                                current_house = (dx, dy)
                                delivery_log.append(f"Tại Nhà #{delivered_count+1}. Minigame Xếp Hàng!")
                    else:
                        delivery_state = "OUT_OF_FUEL"
                        delivery_log.append("HẾT NHIÊN LIỆU!")
                
                if current_step == len(path) - 1 and fuel >= 0 and delivery_state != "OUT_OF_FUEL" and not in_connect4:
                    if delivery_state == "PICKING":
                        in_minigame_caro = True
                        delivery_log.append("Đến Kho. Bắt đầu Caro!")
                    elif delivery_state == "DELIVERING":
                        delivery_state = "RETURNING"
                        current_target = base
                        start = path[-1]
                        algo = choose_algorithm(selected_algo_name)
                        path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                        current_step = 0
                    elif delivery_state == "RETURNING":
                        delivery_state = "IDLE"
                        delivery_log.append("Hoàn thành nhiệm vụ!")

        screen.fill((30, 30, 30))
        
        # Vẽ Panel trái
        panel_x = PADDING
        panel_y = PADDING
        pygame.draw.rect(screen, (40, 40, 40), (panel_x, panel_y, LEFT_PANEL - PADDING, GRID_SIZE * CELL_SIZE))
        screen.blit(bigfont.render('THUẬT TOÁN', True, (200, 200, 200)), (panel_x + 10, panel_y + 10))
        dropdown_y = panel_y + 50
        dropdown_height = font_size + 10
        dropdown_rect = pygame.Rect(panel_x + 10, dropdown_y, LEFT_PANEL - PADDING - 20, dropdown_height)
        pygame.draw.rect(screen, (60, 60, 60), dropdown_rect, 2)
        screen.blit(font.render(selected_algo_name, True, (255, 255, 100)), (panel_x + 15, dropdown_y + 5))
        arrow_x = dropdown_rect.right - 15
        arrow_y = dropdown_rect.centery
        pygame.draw.polygon(screen, (200, 200, 200), [(arrow_x, arrow_y - 3), (arrow_x + 5, arrow_y - 3), (arrow_x + 2.5, arrow_y + 3)])
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
                screen.blit(font.render(opt[:20], True, opt_text_color), (panel_x + 15, opt_y + 3))
                options_rects.append(opt_rect)
        
        diff_title_y = panel_y + 100
        screen.blit(bigfont.render('ĐỘ KHÓ MINIGAME', True, (200, 200, 200)), (panel_x + 10, diff_title_y))
        pygame.draw.rect(screen, (60, 60, 60), diff_rect, 2)
        
        diff_color = (255, 100, 100)
        if DIFFICULTY_LEVELS[current_difficulty_idx] == "DỄ": diff_color = (100, 255, 100)
        elif DIFFICULTY_LEVELS[current_difficulty_idx] == "TRUNG BÌNH": diff_color = (255, 255, 100)
        screen.blit(font.render(DIFFICULTY_LEVELS[current_difficulty_idx], True, diff_color), (panel_x + 15, diff_rect.y + 5))
        
        ctrl_y = panel_y + 200
        screen.blit(font.render('[SPACE] START', True, (200,200,200)), (panel_x + 10, ctrl_y))
        screen.blit(font.render('[R] RANDOM', True, (200,200,200)), (panel_x + 10, ctrl_y + font_size + 5))
        screen.blit(font.render('[ESC] EXIT', True, (200,200,200)), (panel_x + 10, ctrl_y + 2*(font_size + 5)))

        grid_x0 = LEFT_PANEL + PADDING
        grid_y0 = PADDING
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

        for (x, y) in visited:
            pygame.draw.rect(screen, (100, 200, 150), pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
        for (x, y) in path:
            pygame.draw.rect(screen, (230, 220, 100), pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
        for (x, y) in delivered_houses:
            pygame.draw.rect(screen, (120, 180, 255), pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
            pygame.draw.circle(screen, (0, 80, 200), (grid_x0 + y*CELL_SIZE + CELL_SIZE//2, grid_y0 + x*CELL_SIZE + CELL_SIZE//2), max(2, CELL_SIZE//4))

        if current_target is not None and delivery_state in ("DELIVERING", "PICKING", "RETURNING"):
            if isinstance(current_target, list):
                for tx, ty in current_target:
                    pygame.draw.rect(screen, (255, 140, 0), pygame.Rect(grid_x0 + ty*CELL_SIZE, grid_y0 + tx*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1), 2)
            else:
                tx, ty = current_target
                pygame.draw.rect(screen, (255, 140, 0), pygame.Rect(grid_x0 + ty*CELL_SIZE, grid_y0 + tx*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1), 3)

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

        if path and current_step < len(path):
            dx, dy = path[current_step]
            if assets.get('drone'): screen.blit(assets['drone'], (grid_x0 + dy*CELL_SIZE, grid_y0 + dx*CELL_SIZE))
            else: pygame.draw.circle(screen, (255, 0, 0), (grid_x0 + dy*CELL_SIZE + CELL_SIZE//2, grid_y0 + dx*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)
        else:
            sx, sy = start
            if assets.get('drone'): screen.blit(assets['drone'], (grid_x0 + sy*CELL_SIZE, grid_y0 + sx*CELL_SIZE))
            else: pygame.draw.circle(screen, (255, 0, 0), (grid_x0 + sy*CELL_SIZE + CELL_SIZE//2, grid_y0 + sx*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)

        stats_y = panel_y + 300
        screen.blit(bigfont.render('THỐNG KÊ', True, (200,200,200)), (panel_x + 10, stats_y))
        screen.blit(font.render(f"Nodes Visited : {len(visited)}", True, (200,200,200)), (panel_x + 12, stats_y + 36))
        screen.blit(font.render(f"Path Length   : {max(0, len(path)-1)}", True, (200,200,200)), (panel_x + 12, stats_y + 56))
        screen.blit(font.render(f"Total Cost    : {total_cost}", True, (200,200,200)), (panel_x + 12, stats_y + 76))
        screen.blit(font.render(f"Delivered     : {len(delivered_houses)}", True, (200,200,200)), (panel_x + 12, stats_y + 96))
        
        fuel_color = (100, 255, 100)
        if fuel < 20: fuel_color = (255, 100, 100)
        elif fuel < 40: fuel_color = (255, 255, 100)
        screen.blit(font.render(f"Nhiên liệu    : {fuel}", True, fuel_color), (panel_x + 12, stats_y + 116))
        
        # ================= VẼ GIAO DIỆN LOG =================
        log_y = stats_y + 150
        log_rect = pygame.Rect(panel_x + 10, log_y, LEFT_PANEL - PADDING - 10, 170)
        
        # Vẽ viền cho khu vực Log
        pygame.draw.rect(screen, (50, 50, 50), log_rect, border_radius=5)
        screen.blit(bigfont.render('LỊCH SỬ LOG', True, (200,200,200)), (panel_x + 15, log_y + 5))
        
        # Vẽ Text thanh cuộn / Hint
        if len(delivery_log) > max_visible_logs:
            start_idx = log_scroll_offset + 1
            end_idx = min(log_scroll_offset + max_visible_logs, len(delivery_log))
            scroll_text = f"{start_idx}-{end_idx} / {len(delivery_log)}"
            screen.blit(font.render(scroll_text, True, (150,150,150)), (panel_x + 150, log_y + 10))

        # Render các dòng log trong tầm nhìn (Mở rộng số ký tự lên 45 nhờ Panel đã rộng hơn)
        visible_logs = delivery_log[log_scroll_offset : log_scroll_offset + max_visible_logs]
        for i, log_line in enumerate(visible_logs):
            screen.blit(font.render(log_line[:45], True, (200, 200, 200)), (panel_x + 15, log_y + 35 + i*(font_size + 4)))

        # ================= VẼ GIAO DIỆN CARO =================
        if in_minigame_caro:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            board_size = 300
            start_x = screen_width // 2 - board_size // 2
            start_y = screen_height // 2 - board_size // 2
            cell_s = board_size // 3
            
            pygame.draw.rect(screen, (255, 255, 255), (start_x, start_y, board_size, board_size), 5)
            for r in range(3):
                for c in range(3):
                    caro_rects[r][c] = pygame.Rect(start_x + c*cell_s, start_y + r*cell_s, cell_s, cell_s)
                    pygame.draw.rect(screen, (255, 255, 255), caro_rects[r][c], 2)
                    if caro_board[r][c] == 1: screen.blit(bigfont.render("X", True, (255, 100, 100)), (start_x + c*cell_s + cell_s//3, start_y + r*cell_s + cell_s//4))
                    elif caro_board[r][c] == 2: screen.blit(bigfont.render("O", True, (100, 100, 255)), (start_x + c*cell_s + cell_s//3, start_y + r*cell_s + cell_s//4))

        # ================= VẼ GIAO DIỆN CONNECT 4 =================
        if in_connect4:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            pygame.draw.rect(screen, (30, 100, 200), (c4_start_x, c4_start_y, c4_board_width, c4_board_height), border_radius=10)
            
            for r in range(C4_ROWS):
                for c in range(C4_COLS):
                    center_x = int(c4_start_x + c*c4_cell_s + c4_cell_s/2)
                    center_y = int(c4_start_y + r*c4_cell_s + c4_cell_s/2)
                    radius = int(c4_cell_s/2 - 5)
                    
                    color = (20, 20, 20) 
                    if connect4_board[r][c] == PLAYER_C4: color = (255, 50, 50) 
                    elif connect4_board[r][c] == AI_C4: color = (255, 255, 50) 
                    pygame.draw.circle(screen, color, (center_x, center_y), radius)
            
            title_text = bigfont.render("XẾP HÀNG - CLICK VÀO CỘT ĐỂ THẢ", True, (255, 255, 255))
            screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, c4_start_y - 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()