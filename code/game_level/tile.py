import pygame
from settings.settings import *

class Tile(pygame.sprite.Sprite):
    """Lớp biểu diễn cho một object trên bản đồ. 
        Kích thước 1 tile là 64x64 pixel
    """
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.y_offset = HITBOX_OFFSET.get(self.sprite_type)
        # Adjusing size of Large Object (128 pixel for either the height of width) 
        # to AVOID OVERLAPPING with smaller objects on the Y axis
        if self.sprite_type == 'large_object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, self.y_offset) # set hitbox collider to draw overlapping sprite