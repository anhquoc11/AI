import pygame
def draw_algorithm_dropdown(screen,font,dropdown_rect,algo_options,dropdown_scroll_offset,max_visible_items,selected_algo_name,LEFT_PANEL,PADDING,font_size):
    visible_items = algo_options[dropdown_scroll_offset:dropdown_scroll_offset + max_visible_items]
    list_height = len(visible_items) * (font_size + 5)
    if len(algo_options) > max_visible_items: list_height += font_size + 5
            
    shadow_rect = pygame.Rect(PADDING + 13, dropdown_rect.bottom + 3, LEFT_PANEL - PADDING - 20, list_height)
    pygame.draw.rect(screen, (20, 20, 20), shadow_rect)
            
    bg_rect = pygame.Rect(PADDING + 10, dropdown_rect.bottom, LEFT_PANEL - PADDING - 20, list_height)
    pygame.draw.rect(screen, (50, 50, 50), bg_rect)
    pygame.draw.rect(screen, (200, 200, 200), bg_rect, 1)

    for i, opt in enumerate(visible_items):
        opt_y = dropdown_rect.bottom + i * (font_size + 5)
        opt_rect = pygame.Rect(PADDING + 10, opt_y, LEFT_PANEL - PADDING - 20, font_size + 5)
        opt_color = (100, 100, 150) if opt == selected_algo_name else (70, 70, 70)
        pygame.draw.rect(screen, opt_color, opt_rect)
        pygame.draw.rect(screen, (200, 200, 200), opt_rect, 1)
        opt_text_color = (255, 255, 100) if opt == selected_algo_name else (200, 200, 200)
        screen.blit(font.render(opt[:20], True, opt_text_color), (PADDING + 15, opt_y + 3))
            
    if len(algo_options) > max_visible_items:
        scroll_bg_rect = pygame.Rect(PADDING + 10, dropdown_rect.bottom + max_visible_items * (font_size + 5), LEFT_PANEL - PADDING - 20, font_size + 5)
        pygame.draw.rect(screen, (50, 50, 50), scroll_bg_rect)
        pygame.draw.rect(screen, (200, 200, 200), scroll_bg_rect, 1)
        scroll_text = f"UP/DOWN {dropdown_scroll_offset+1}/{len(algo_options)}"
        screen.blit(font.render(scroll_text, True, (150, 150, 100)), (PADDING + 15, scroll_bg_rect.y + 3))

def draw_pack_dropdown(screen,font,pack_dropdown_rect,pack_options,selected_pack_name,LEFT_PANEL,PADDING,font_size):
    list_height = len(pack_options) * (font_size + 5)
    shadow_rect = pygame.Rect(PADDING + 13, pack_dropdown_rect.bottom + 3, LEFT_PANEL - PADDING - 20, list_height)
    pygame.draw.rect(screen, (20, 20, 20), shadow_rect)
            
    bg_rect = pygame.Rect(PADDING + 10, pack_dropdown_rect.bottom, LEFT_PANEL - PADDING - 20, list_height)
    pygame.draw.rect(screen, (50, 50, 50), bg_rect)
    pygame.draw.rect(screen, (200, 200, 200), bg_rect, 1)

    for i, opt in enumerate(pack_options):
        opt_y = pack_dropdown_rect.bottom + i * (font_size + 5)
        opt_rect = pygame.Rect(PADDING + 10, opt_y, LEFT_PANEL - PADDING - 20, font_size + 5)
        opt_color = (100, 100, 150) if opt == selected_pack_name else (70, 70, 70)
        pygame.draw.rect(screen, opt_color, opt_rect)
        pygame.draw.rect(screen, (200, 200, 200), opt_rect, 1)
        opt_text_color = (255, 255, 100) if opt == selected_pack_name else (200, 200, 200)
        screen.blit(font.render(opt[:20], True, opt_text_color), (PADDING + 15, opt_y + 3))