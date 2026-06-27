import pygame 


def draw_knapsack_animation(pack_history,pack_think_step,grid_x0,grid_y0,GRID_WIDTH,GRID_HEIGHT,screen,bigfont,pack_capacity,font):
    curr_sub, curr_w, curr_v, status = pack_history[pack_think_step]
            
    panel_w, panel_h = 420, 180
    px = grid_x0 + (GRID_WIDTH - panel_w) // 2
    py = grid_y0 + (GRID_HEIGHT - panel_h) // 2
            
    pygame.draw.rect(screen, (40, 40, 40), (px, py, panel_w, panel_h), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), (px, py, panel_w, panel_h), 2, border_radius=10)
            
    screen.blit(bigfont.render("ĐANG BỐC HÀNG VÀO DRONE", True, (255, 255, 100)), (px + 20, py + 15))
            
    bar_w = 380
    bar_h = 30
    pygame.draw.rect(screen, (80, 80, 80), (px + 20, py + 60, bar_w, bar_h))
            
    fill_w = min(bar_w, int(bar_w * (curr_w / pack_capacity))) if pack_capacity > 0 else 0
    bar_color = (100, 255, 100) if curr_w <= pack_capacity else (255, 100, 100)
    pygame.draw.rect(screen, bar_color, (px + 20, py + 60, fill_w, bar_h))
            
    screen.blit(font.render(f"Trọng lượng : {curr_w} / {pack_capacity} kg", True, (255, 255, 255)), (px + 25, py + 65))
    screen.blit(font.render(f"Giá trị đơn : {curr_v} $", True, (255, 200, 100)), (px + 20, py + 105))
            
    status_text = "Đang thử xếp tổ hợp này..."
    status_color = (255, 255, 100)
    if status == "PRUNED_OVERWEIGHT":
        status_text = "Quá nặng! Thử kiện hàng khác..."
        status_color = (255, 100, 100)
    elif status == "RECORD":
        status_text = "Vừa vặn! Tạm ghi nhớ tổ hợp này."
        status_color = (100, 255, 100)
                
    screen.blit(font.render(status_text, True, status_color), (px + 20, py + 140))