import pygame 
from .settings import ASSET_PATH 
def load_assets(cell_size):
    def load(name, custom_size=None):
        try:
            img = pygame.image.load(ASSET_PATH + name)
            if custom_size:
                return pygame.transform.scale(img, custom_size)
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
        'c4_player': load('box.png', (60, 60)), 
        'c4_ai': load('lock.png', (60, 60))
    }
