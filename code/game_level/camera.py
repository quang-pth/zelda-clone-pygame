import pygame

# Sorting Sprite by the Y Coordinates to perform overlaping by the Camera
class YSortCameraGroup(pygame.sprite.Group):
    """Lớp camera chính để render bản đồ cho game.
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # Creating the floor
        self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0, 0))

    def custom_draw(self, player):
        """Vẽ các object trong game theo thứ tự trên trục y.
        
        (method) custom_draw(player: Player) -> None 
        """
        # Getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # Drawing the floor and offset it
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        # Drawing other entities including rocks, obstacles, enemies,...
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            # Displaying each sprite according to the offset position
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    
    def enemy_update(self, player):
        """Cập nhật trạng thái các object có thể tấn công được cho người chơi.
        
        (method) enemy_update(player: Player) -> None 
        """
        enemy_sprites = [sprite for sprite in self.sprites() if (hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy')]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)