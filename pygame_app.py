import pygame
import sys
import random
from config.settings import *
from config.assets import load_assets
from core.map_generator import random_map
from core.movement import *
from ui.map import *
from ui.panels import *
from ui.map_draw import *
from ui.dropdown import *
from ui.knapsack_ui import *
from ui.caro_ui import *
from ui.connect4_ui import *
from algorithms.backtracking import knapsack_backtracking
from algorithms.forward_checking import knapsack_forward_checking
from core.algorithm_registry import choose_algorithm, ALG_MAP
from core.map_manager import create_map
from core.game_logic import * 

def main():
    pygame.init()
    
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Delivery Game")
    clock = pygame.time.Clock()
    
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
    grid, start, goal, warehouse_orders = create_map(GRID_SIZE)
    base = start
    
    selected_algo_name = 'A*'
    algo = choose_algorithm(selected_algo_name)
    algo_options = list(ALG_MAP.keys())
    dropdown_open = False
    dropdown_scroll_offset = 0
    max_visible_items = 5
    
    pack_options = ["Backtracking", "Forward Checking"]
    selected_pack_name = pack_options[0]
    pack_dropdown_open = False
    
    path = []
    visited = set()
    total_cost = 0
    runtime_ms = 0
    running = True
    
    delivery_state = "IDLE"
    current_target = None
    
    delivery_log = []
    log_scroll_offset = 0
    max_visible_logs = 6
    prev_log_length = 0
    log_rect = pygame.Rect(0, 0, 0, 0) 
    
    delivered_count = 0
    delivered_houses = []
    
    caro_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    in_minigame_caro = False
    caro_player_turn = True
    caro_rects = [[None for _ in range(3)] for _ in range(3)]
    
    connect4_board = [[EMPTY for _ in range(C4_COLS)] for _ in range(C4_ROWS)]
    in_connect4 = False
    c4_player_turn = True
    current_house = None
    
    current_difficulty_idx = 2 
    
    fuel = 60

    current_step = 0
    move_timer = 0
    ai_timer = 0 
    
    pack_history = []
    pack_best_route = None
    pack_think_step = 0
    pack_think_timer = 0
    pack_capacity = 15

    while running:
        now = pygame.time.get_ticks()
        
        # Calculate GUI boundaries
        dropdown_height = font_size + 10
        algo_title_y = PADDING + 10
        dropdown_y = algo_title_y + 30
        dropdown_rect = pygame.Rect(PADDING + 10, dropdown_y, LEFT_PANEL - PADDING - 20, dropdown_height)
        
        pack_title_y = dropdown_rect.bottom + 15
        pack_dropdown_y = pack_title_y + 30
        pack_dropdown_rect = pygame.Rect(PADDING + 10, pack_dropdown_y, LEFT_PANEL - PADDING - 20, dropdown_height)
        
        diff_title_y = pack_dropdown_rect.bottom + 15
        diff_rect_y = diff_title_y + 30
        diff_rect = pygame.Rect(PADDING + 10, diff_rect_y, LEFT_PANEL - PADDING - 20, font_size + 10)
        
        ctrl_y = diff_rect.bottom + 20
        stats_y = ctrl_y + 80
        log_y = stats_y + 190 
        
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
                LEFT_PANEL = max(380, int(screen_width * 0.28))
                GRID_WIDTH = screen_width - LEFT_PANEL - 3 * PADDING
                GRID_HEIGHT = screen_height - 2 * PADDING
                CELL_SIZE = min(GRID_WIDTH // GRID_SIZE, GRID_HEIGHT // GRID_SIZE)
                assets = load_assets(CELL_SIZE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_dropdown = False
                    
                    if dropdown_open:
                        visible_items = algo_options[dropdown_scroll_offset:dropdown_scroll_offset + max_visible_items]
                        for i, opt in enumerate(visible_items):
                            opt_rect = pygame.Rect(PADDING + 10, dropdown_rect.bottom + i * (font_size + 5), LEFT_PANEL - PADDING - 20, font_size + 5)
                            if opt_rect.collidepoint(event.pos):
                                selected_algo_name = opt
                                algo = choose_algorithm(selected_algo_name)
                                dropdown_open = False
                                clicked_dropdown = True
                                break
                    if dropdown_rect.collidepoint(event.pos) and not clicked_dropdown and not pack_dropdown_open:
                        dropdown_open = not dropdown_open
                        dropdown_scroll_offset = 0
                        clicked_dropdown = True

                    if pack_dropdown_open and not clicked_dropdown:
                        for i, opt in enumerate(pack_options):
                            opt_rect = pygame.Rect(PADDING + 10, pack_dropdown_rect.bottom + i * (font_size + 5), LEFT_PANEL - PADDING - 20, font_size + 5)
                            if opt_rect.collidepoint(event.pos):
                                selected_pack_name = opt
                                pack_dropdown_open = False
                                clicked_dropdown = True
                                break
                    if pack_dropdown_rect.collidepoint(event.pos) and not clicked_dropdown and not dropdown_open:
                        pack_dropdown_open = not pack_dropdown_open
                        clicked_dropdown = True

                    if not clicked_dropdown:
                        dropdown_open = False 
                        pack_dropdown_open = False
                            
                        if not in_minigame_caro and not in_connect4 and diff_rect.collidepoint(event.pos):
                            current_difficulty_idx = (current_difficulty_idx + 1) % len(DIFFICULTY_LEVELS)
                        
                        elif in_minigame_caro and caro_player_turn:
                            mx, my = event.pos
                            for r in range(3):
                                for c in range(3):
                                    if caro_rects[r][c] and caro_rects[r][c].collidepoint((mx, my)) and caro_board[r][c] == 0:
                                        caro_board[r][c] = 1
                                        caro_player_turn = False
                                        ai_timer = pygame.time.get_ticks() 
                        
                        elif in_connect4 and c4_player_turn:
                            mx, my = event.pos
                            if c4_start_x <= mx <= c4_start_x + c4_board_width and c4_start_y <= my <= c4_start_y + c4_board_height:
                                col = (mx - c4_start_x) // c4_cell_s
                                row = get_next_open_row(connect4_board, col)
                                if row != -1:
                                    connect4_board[row][col] = PLAYER_C4
                                    c4_player_turn = False
                                    ai_timer = pygame.time.get_ticks() 

                elif event.button == 4: 
                    if dropdown_open: dropdown_scroll_offset = max(0, dropdown_scroll_offset - 1)
                    elif log_rect.collidepoint(event.pos): log_scroll_offset = max(0, log_scroll_offset - 1)
                elif event.button == 5: 
                    if dropdown_open: dropdown_scroll_offset = min(max(0, len(algo_options) - max_visible_items), dropdown_scroll_offset + 1)
                    elif log_rect.collidepoint(event.pos): log_scroll_offset = min(max(0, len(delivery_log) - max_visible_logs), log_scroll_offset + 1)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    grid = random_map(GRID_SIZE, obstacle_prob=0.12)
                    start = None
                    goal = None
                    warehouse_orders = []
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            if grid[i][j] == 3: start = (i, j)
                            elif grid[i][j] == 4: goal = (i, j)
                            elif grid[i][j] == 5: 
                                grid[i][j] = 0
                                warehouse_orders.append({'w': random.randint(3, 7), 'v': random.randint(10, 50), 'pos': (i, j)})
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
                    pack_dropdown_open = False
                    houses = []
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
                        if warehouse_orders:
                            start = base
                            delivery_state = "PICKING"
                            delivery_log.append("Bay tới Kho lấy hàng...")
                            delivered_count = 0
                            delivered_houses = []
                            current_target = goal
                            current_step = 0
                            algo = choose_algorithm(selected_algo_name)
                            path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                            if not path:
                                delivery_state = "IDLE"
                            move_timer = pygame.time.get_ticks()
                        else:
                            delivery_log.append("Kho đã giao hết hàng!")

        if len(delivery_log) != prev_log_length:
            log_scroll_offset = max(0, len(delivery_log) - max_visible_logs)
            prev_log_length = len(delivery_log)

        # ================= AI CARO & QUYẾT ĐỊNH TẢI TRỌNG =================
        if in_minigame_caro and not caro_player_turn and (now - ai_timer > 300):
            caro_player_turn, fuel =  update_caro(caro_board,current_difficulty_idx,DIFFICULTY_LEVELS,fuel)

        if in_minigame_caro and is_terminal_caro(caro_board):
            pygame.time.delay(1000)
            winner = check_winner_caro(caro_board)
            pack_capacity = MAX_WEIGHT
            
            if winner == 1:
                fuel += 50
                delivery_log.append("Caro Thắng! Lấy tối đa tải trọng")
            elif winner == 2:
                if DIFFICULTY_LEVELS[current_difficulty_idx] == "KHÓ":
                    delivery_log.append("Caro Thua (Khó)! Hủy chuyến giao!")
                    delivery_state = "IDLE"
                    in_minigame_caro = False
                    caro_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                    caro_player_turn = True
                    continue 
                else:
                    pack_capacity = MAX_WEIGHT // 2 
                    delivery_log.append(f"Caro Thua! Phạt chỉ lấy {pack_capacity}kg")
            else:
                fuel += 20
                delivery_log.append("Caro Hòa! Lấy tối đa tải trọng")

            in_minigame_caro = False
            caro_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            caro_player_turn = True
            
            if selected_pack_name == "Backtracking":
                pack_best_route, pack_history = knapsack_backtracking(warehouse_orders, pack_capacity)
            else:
                pack_best_route, pack_history = knapsack_forward_checking(warehouse_orders, pack_capacity)
                
            delivery_state = "THINKING_PACK"
            pack_think_step = 0
            pack_think_timer = pygame.time.get_ticks()

        # ================= CHẠY ANIMATION SẮP XẾP HÀNG (KNAPSACK) =================
        if delivery_state == "THINKING_PACK":
            if now - pack_think_timer > 250: 
                if pack_think_step < len(pack_history):
                    curr_sub, curr_w, curr_v, status = pack_history[pack_think_step]
                    
                    if status == "PRUNED_OVERWEIGHT":
                        delivery_log.append(f"[QUÁ TẢI] Loại phương án {curr_w}kg")
                    elif status == "RECORD":
                        delivery_log.append(f"[KỶ LỤC] Thử chọn {len(curr_sub)} đơn ({curr_v}$)")
                    elif status == "THINKING":
                        delivery_log.append(f"[ĐANG XẾP] {len(curr_sub)} đơn (Nặng: {curr_w}kg)")
                        
                pack_think_timer = now
                pack_think_step += 1
                
                if pack_think_step >= len(pack_history):
                    selected_orders = pack_best_route
                    if not selected_orders:
                        delivery_log.append("Đơn còn lại quá nặng! Không bốc được")
                        delivery_state = "IDLE"
                    else:
                        total_w = sum(o['w'] for o in selected_orders)
                        total_v = sum(o['v'] for o in selected_orders)
                        delivery_log.append(f"XONG! Bốc {len(selected_orders)} đơn ({total_w}kg - {total_v}$)")
                        houses = []
                        for o in selected_orders:
                            houses.append(o['pos'])
                            grid[o['pos'][0]][o['pos'][1]] = 5 
                        current_target = houses
                        drone_pos = path[current_step] if path else base
                        start = drone_pos
                        algo = choose_algorithm(selected_algo_name)
                        path, total_cost, visited, runtime_ms = compute_path_to_target(
                            start,
                            current_target,
                            grid,
                            algo
                            )
                        safe_orders, safe_cost, ao_history = find_safe_orders(selected_orders,fuel,grid,start,algo)
                        for item in ao_history:
                            orders = ", ".join(str(order["pos"]) for order in item["orders"])
                            if item["safe"]: delivery_log.append(f"[AO] ({orders}) -> AN TOÀN")
                            else: delivery_log.append(f"[AO] ({orders}) -> KHÔNG AN TOÀN")
                        if safe_orders:
                            houses = [o['pos'] for o in safe_orders]
                            current_target = houses
                            current_step = 0
                            drone_pos = start
                            path, total_cost, visited, runtime_ms = compute_path_to_target(start,current_target,grid,algo)
                            for o in safe_orders:
                                if o in warehouse_orders:
                                    warehouse_orders.remove(o)
                            delivery_log.append(f"[AO] Chọn {len(safe_orders)}/{len(selected_orders)} đơn an toàn")
                            delivery_state = "DELIVERING"
                            move_timer = pygame.time.get_ticks()
                        else:
                            delivery_log.append("[AO] Không tìm được phương án giao an toàn")
                            delivery_state = "IDLE"
        # ================= AI CONNECT 4 =================
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
                delivery_log.append("Giao hàng & Xếp Thua! -10 Nhiên liệu")
                if fuel < 0:
                    fuel = 0
            c4_player_turn = True
            in_connect4 = False
            connect4_board = [[EMPTY for _ in range(C4_COLS)] for _ in range(C4_ROWS)]
            
            delivered_count += 1
            delivered_houses.append(current_house)
            houses = [h for h in houses if h != current_house]
            grid[current_house[0]][current_house[1]] = 0 
            current_house = None
            
            if houses:
                current_target = houses
                drone_pos = path[current_step] if path else base
                start = drone_pos
                algo = choose_algorithm(selected_algo_name)
                path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                current_step = 0
            else:
                if warehouse_orders:
                    delivery_state = "RETURNING"
                    current_target = goal
                    delivery_log.append("Vẫn còn hàng trong kho. Đang bay về!")
                else:
                    delivery_state = "RETURNING"
                    current_target = base
                    delivery_log.append("Giao hết mọi đơn. Quay về vị trí ban đầu!")
                    
                drone_pos = path[current_step] if path else base
                start = drone_pos
                algo = choose_algorithm(selected_algo_name)
                path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                current_step = 0
                
            move_timer = pygame.time.get_ticks()

        # ================= MOVEMENT DRONE =================
        if path and delivery_state not in ("IDLE", "OUT_OF_FUEL", "THINKING_PACK") and not in_minigame_caro and not in_connect4:
            if now - move_timer > 150:
                move_timer = now
                if current_step < len(path) - 1:
                    next_x, next_y = path[current_step + 1]
                    cost = movement_cost(grid[next_x][next_y])
                    if fuel >= cost:
                        fuel -= cost
                        current_step += 1
                        dx, dy = path[current_step]
                    else:
                        delivery_state = "OUT_OF_FUEL"
                        delivery_log.append("HẾT NHIÊN LIỆU!")
                        continue
                        
                    if delivery_state == "DELIVERING":
                        if (dx, dy) in houses and (dx, dy) not in delivered_houses:
                            in_connect4 = True
                            current_house = (dx, dy)
                            delivery_log.append(f"Tại Nhà #{delivered_count+1}. Minigame Xếp Hàng!")
                
                if current_step == len(path) - 1 and fuel >= 0 and delivery_state != "OUT_OF_FUEL" and not in_connect4:
                    if delivery_state == "PICKING":
                        in_minigame_caro = True
                        delivery_log.append("Đến Kho. Bắt đầu Truy cập kho!")
                    elif delivery_state == "RETURNING":
                        if warehouse_orders:
                            in_minigame_caro = True
                            delivery_state = "PICKING"
                            delivery_log.append("Đã về kho. Truy cập bốc mẻ tiếp theo!")
                        else:
                            delivery_state = "IDLE"
                            delivery_log.append("Hoàn thành mọi nhiệm vụ trong ngày!")

        screen.fill((30, 30, 30))
        
        # ================= VẼ BẢNG ĐIỀU KHIỂN BÊN TRÁI =================
        panel_x = PADDING
        panel_y = PADDING
        draw_panel_background(screen,panel_x,panel_y,LEFT_PANEL,PADDING,GRID_SIZE,CELL_SIZE)
        draw_algorithm_panel(screen,bigfont,font,panel_x,dropdown_rect,algo_title_y,selected_algo_name)
        draw_packing_panel(screen,bigfont,font,panel_x,pack_title_y,pack_dropdown_rect,selected_pack_name)
        draw_difficulty_panel(screen,bigfont,font,panel_x,diff_title_y,diff_rect,DIFFICULTY_LEVELS,current_difficulty_idx)
        draw_control_panel(screen,font,panel_x,ctrl_y,font_size)
        draw_statistics_panel(screen,bigfont,font,panel_x,stats_y,visited,path,total_cost,runtime_ms,warehouse_orders,delivered_houses,fuel)
        log_rect = draw_log_panel(screen,bigfont,font,panel_x,log_y,LEFT_PANEL,PADDING,screen_height,delivery_log,log_scroll_offset,font_size)

        # ================= VẼ LƯỚI BẢN ĐỒ BÊN PHẢI =================
        grid_x0 = LEFT_PANEL + PADDING + (GRID_WIDTH - GRID_SIZE * CELL_SIZE) // 2
        grid_y0 = PADDING + (GRID_HEIGHT - GRID_SIZE * CELL_SIZE) // 2
        draw_cells(screen,grid,GRID_SIZE,CELL_SIZE,grid_x0,grid_y0)
        draw_visited(visited,screen,grid_x0,grid_y0,CELL_SIZE)
        draw_path(path,screen,grid_x0,grid_y0,CELL_SIZE)
        draw_delivered(delivered_houses,screen,grid_x0,grid_y0,CELL_SIZE)
        draw_targets(screen,current_target,delivery_state,CELL_SIZE,grid_x0,grid_y0)
        draw_objects(assets,GRID_SIZE,grid,grid_x0,grid_y0,CELL_SIZE,screen)
        draw_drone(assets,path,current_step ,grid_x0,grid_y0,CELL_SIZE,screen,start)
        # ================= VẼ DANH SÁCH ĐƠN HÀNG TRONG KHO (HUD) =================
        draw_warehouse_panel(screen,font,warehouse_orders,screen_width,PADDING)

        # ================= VẼ GIAO DIỆN CHỜ XẾP HÀNG LÊN DRONE =================
        if delivery_state == "THINKING_PACK" and pack_think_step < len(pack_history):
            draw_knapsack_animation(pack_history,pack_think_step,grid_x0,grid_y0,GRID_WIDTH,GRID_HEIGHT,screen,bigfont,pack_capacity,font)

        # ================= VẼ GIAO DIỆN CARO =================
        if in_minigame_caro:
            draw_caro(screen,screen_width,screen_height,bigfont,caro_board,caro_rects)
        # ================= VẼ GIAO DIỆN CONNECT 4 BẰNG ẢNH =================
        if in_connect4:
            draw_connect4(screen,screen_width,screen_height,bigfont,connect4_board,assets,c4_start_x, c4_start_y, c4_board_width, c4_board_height,C4_ROWS,C4_COLS,c4_cell_s,EMPTY,PLAYER_C4,AI_C4)
        # ================= VẼ CÁC DROPDOWN MENU (NỔI LÊN TRÊN CÙNG) =================
        if dropdown_open: draw_algorithm_dropdown(screen,font,dropdown_rect,algo_options,dropdown_scroll_offset,max_visible_items,selected_algo_name,LEFT_PANEL,PADDING,font_size)

        if pack_dropdown_open: draw_pack_dropdown(screen,font,pack_dropdown_rect,pack_options,selected_pack_name,LEFT_PANEL,PADDING,font_size)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()