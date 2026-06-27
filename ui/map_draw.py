import pygame

def draw_warehouse_panel(screen,font,warehouse_orders,screen_width,PADDING):
    if warehouse_orders:
            wh_panel_w = 200
            wh_panel_h = 40 + len(warehouse_orders) * 25
            wh_px = screen_width - wh_panel_w - PADDING
            wh_py = PADDING
            
            wh_surface = pygame.Surface((wh_panel_w, wh_panel_h))
            wh_surface.set_alpha(220)
            wh_surface.fill((40, 40, 40))
            screen.blit(wh_surface, (wh_px, wh_py))
            pygame.draw.rect(screen, (200, 200, 200), (wh_px, wh_py, wh_panel_w, wh_panel_h), 1, border_radius=5)
            
            screen.blit(font.render("HÀNG TRONG KHO", True, (255, 200, 100)), (wh_px + 15, wh_py + 10))
            for idx, order in enumerate(warehouse_orders):
                item_txt = f"Kiện {idx+1}: {order['w']}kg  -  {order['v']}$"
                screen.blit(font.render(item_txt, True, (220, 220, 220)), (wh_px + 15, wh_py + 35 + idx*25))

     