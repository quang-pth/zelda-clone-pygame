import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    """Lớp chung cho lớp Player và Enemy (hay các thực thể trong game)"""
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_idx = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        """Di chuyển thực thể dựa trên tốc độ
        
        (method) move(speed: float) -> None
        """
        # Ensuring player move with the same speed for all directions
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Tính hitbox để gây sát thương dựa trên hướng di chuyển của thực thể
        
        (method) collisiion(direction: str) -> None 
        """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # player moving RIGHT
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # player moving LEFT
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # player moving DOWN
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # player moving UP
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        """Lấy giá trị alpha để chạy hiệu ứng miễn giảm sát thương
        
        (method) wave_value() -> int 
        """
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0