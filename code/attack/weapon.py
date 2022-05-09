import pygame

class Weapon(pygame.sprite.Sprite):
    """Lớp chứa thông tin về các đòn tấn công vật lí của người chơi.
    Có 4 loại vũ khí: axe, lance, rapier, sai và sword."""
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        # Player Direction
        direction = player.status.split('_')[0]
        # Graphic
        full_path = f'graphics/weapons/{player.using_weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        # Placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(center = player.rect.center)