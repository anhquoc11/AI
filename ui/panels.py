import pygame 

def draw_panel_background(screen,panel_x,panel_y,LEFT_PANEL,PADDING,GRID_SIZE,CELL_SIZE):
    pygame.draw.rect(screen,(40,40,40),(panel_x,panel_y,LEFT_PANEL-PADDING,GRID_SIZE*CELL_SIZE))

def draw_algorithm_panel(screen,bigfont,font,panel_x,dropdown_rect,algo_title_y,selected_algo_name):
    screen.blit(bigfont.render('THUẬT TOÁN TÌM ĐƯỜNG', True, (200, 200, 200)), (panel_x + 10, algo_title_y))
    pygame.draw.rect(screen, (60, 60, 60), dropdown_rect, 2)
    screen.blit(font.render(selected_algo_name, True, (255, 255, 100)), (panel_x + 15, dropdown_rect.y + 5))
    pygame.draw.polygon(screen, (200, 200, 200), [(dropdown_rect.right - 15, dropdown_rect.centery - 3), (dropdown_rect.right - 10, dropdown_rect.centery - 3), (dropdown_rect.right - 12.5, dropdown_rect.centery + 3)])


def draw_packing_panel(screen,bigfont,font,panel_x,pack_title_y,pack_dropdown_rect,selected_pack_name):
    screen.blit(bigfont.render('SẮP XẾP HÀNG (KNAPSACK)', True, (200, 200, 200)), (panel_x + 10, pack_title_y))
    pygame.draw.rect(screen, (60, 60, 60), pack_dropdown_rect, 2)
    screen.blit(font.render(selected_pack_name, True, (255, 255, 100)), (panel_x + 15, pack_dropdown_rect.y + 5))
    pygame.draw.polygon(screen, (200, 200, 200), [(pack_dropdown_rect.right - 15, pack_dropdown_rect.centery - 3), (pack_dropdown_rect.right - 10, pack_dropdown_rect.centery - 3), (pack_dropdown_rect.right - 12.5, pack_dropdown_rect.centery + 3)])

def draw_difficulty_panel(screen,bigfont,font,panel_x,diff_title_y,diff_rect,DIFFICULTY_LEVELS,current_difficulty_idx):
    screen.blit(bigfont.render('ĐỘ KHÓ MINIGAME', True, (200, 200, 200)), (panel_x + 10, diff_title_y))
    pygame.draw.rect(screen, (60, 60, 60), diff_rect, 2)
    diff_color = (255, 100, 100)
    if DIFFICULTY_LEVELS[current_difficulty_idx] == "DỄ": diff_color = (100, 255, 100)
    elif DIFFICULTY_LEVELS[current_difficulty_idx] == "TRUNG BÌNH": diff_color = (255, 255, 100)
    screen.blit(font.render(DIFFICULTY_LEVELS[current_difficulty_idx], True, diff_color), (panel_x + 15, diff_rect.y + 5))

def draw_control_panel(screen,font,panel_x,ctrl_y,font_size):
    screen.blit(font.render('[SPACE] START', True, (200,200,200)), (panel_x + 10, ctrl_y))
    screen.blit(font.render('[R] RANDOM', True, (200,200,200)), (panel_x + 10, ctrl_y + font_size + 5))
    screen.blit(font.render('[ESC] EXIT', True, (200,200,200)), (panel_x + 10, ctrl_y + 2*(font_size + 5)))

def draw_statistics_panel(screen,bigfont,font,panel_x,stats_y,visited,path,total_cost,runtime_ms,warehouse_orders,delivered_houses,fuel):
    screen.blit(bigfont.render('THỐNG KÊ', True, (200,200,200)), (panel_x + 10, stats_y))
    screen.blit(font.render(f"Nodes Visited : {len(visited)}", True, (200,200,200)), (panel_x + 12, stats_y + 36))
    screen.blit(font.render(f"Path Length   : {max(0, len(path)-1)}", True, (200,200,200)), (panel_x + 12, stats_y + 56))
    screen.blit(font.render(f"Total Cost    : {total_cost}", True, (200,200,200)), (panel_x + 12, stats_y + 76))
    screen.blit(font.render(f"Runtime       : {runtime_ms} ms", True, (200,200,200)), (panel_x + 12, stats_y + 96))
    screen.blit(font.render(f"Kho chờ giao  : {len(warehouse_orders)} đơn", True, (255,200,100)), (panel_x + 12, stats_y + 116))
    screen.blit(font.render(f"Đã giao xong  : {len(delivered_houses)} đơn", True, (200,200,200)), (panel_x + 12, stats_y + 136))
    fuel_color = (100, 255, 100)
    if fuel < 20: fuel_color = (255, 100, 100)
    elif fuel < 40: fuel_color = (255, 255, 100)
    screen.blit(font.render(f"Nhiên liệu    : {fuel}", True, fuel_color), (panel_x + 12, stats_y + 156))

def draw_log_panel(screen,bigfont,font,panel_x,log_y,LEFT_PANEL,PADDING,screen_height,delivery_log,log_scroll_offset,font_size):
    log_rect = pygame.Rect(panel_x + 10, log_y, LEFT_PANEL - PADDING - 10, screen_height - log_y - PADDING)
    pygame.draw.rect(screen, (50, 50, 50), log_rect, border_radius=5)
    screen.blit(bigfont.render('LỊCH SỬ LOG', True, (200,200,200)), (panel_x + 15, log_y + 5))
        
    max_visible_logs = (log_rect.height - 40) // (font_size + 4)
    if len(delivery_log) > max_visible_logs:
        start_idx = log_scroll_offset + 1
        end_idx = min(log_scroll_offset + max_visible_logs, len(delivery_log))
        scroll_text = f"{start_idx}-{end_idx} / {len(delivery_log)}"
        screen.blit(font.render(scroll_text, True, (150,150,150)), (panel_x + LEFT_PANEL - 120, log_y + 10))

    visible_logs = delivery_log[log_scroll_offset : log_scroll_offset + max_visible_logs]
    for i, log_line in enumerate(visible_logs):
        screen.blit(font.render(log_line[:45], True, (200, 200, 200)), (panel_x + 15, log_y + 35 + i*(font_size + 4)))
    return log_rect