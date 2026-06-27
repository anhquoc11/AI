import pygame

def draw_connect4(screen,screen_width,screen_height,bigfont,connect4_board,assets,c4_start_x, c4_start_y, c4_board_width, c4_board_height,C4_ROWS,C4_COLS,c4_cell_s,EMPTY,PLAYER_C4,AI_C4):
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
                    
            if connect4_board[r][c] == EMPTY:
                pygame.draw.circle(screen, (20, 20, 20), (center_x, center_y), radius)
            elif connect4_board[r][c] == PLAYER_C4:
                if assets.get('c4_player'):
                    img_rect = assets['c4_player'].get_rect(center=(center_x, center_y))
                    screen.blit(assets['c4_player'], img_rect)
                else:
                    pygame.draw.circle(screen, (255, 50, 50), (center_x, center_y), radius)
            elif connect4_board[r][c] == AI_C4:
                if assets.get('c4_ai'):
                    img_rect = assets['c4_ai'].get_rect(center=(center_x, center_y))
                    screen.blit(assets['c4_ai'], img_rect)
                else:
                    pygame.draw.circle(screen, (255, 255, 50), (center_x, center_y), radius)
            
        title_text = bigfont.render("XẾP HÀNG - CLICK VÀO CỘT ĐỂ THẢ", True, (255, 255, 255))
        screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, c4_start_y - 40))