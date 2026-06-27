import pygame 

def draw_caro(screen,screen_width,screen_height,bigfont,caro_board,caro_rects):
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
            
    board_size = 300
    start_x = screen_width // 2 - board_size // 2
    start_y = screen_height // 2 - board_size // 2
    cell_s = board_size // 3
            
    caro_title = bigfont.render("TRUY CẬP KHO", True, (255, 255, 100))
    screen.blit(caro_title, (screen_width // 2 - caro_title.get_width() // 2, start_y - 40))
            
    pygame.draw.rect(screen, (255, 255, 255), (start_x, start_y, board_size, board_size), 5)
    for r in range(3):
        for c in range(3):
            caro_rects[r][c] = pygame.Rect(start_x + c*cell_s, start_y + r*cell_s, cell_s, cell_s)
            pygame.draw.rect(screen, (255, 255, 255), caro_rects[r][c], 2)
            if caro_board[r][c] == 1: screen.blit(bigfont.render("X", True, (255, 100, 100)), (start_x + c*cell_s + cell_s//3, start_y + r*cell_s + cell_s//4))
            elif caro_board[r][c] == 2: screen.blit(bigfont.render("O", True, (100, 100, 255)), (start_x + c*cell_s + cell_s//3, start_y + r*cell_s + cell_s//4))
