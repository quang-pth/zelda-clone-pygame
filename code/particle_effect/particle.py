import pygame

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, sprite_type = 'magic'):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.frame_idx = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_idx]
        self.rect = self.image.get_rect(center = pos)
    
    def animate(self):
        self.frame_idx += self.animation_speed
        if self.frame_idx >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_idx)]
    
    def update(self):
        self.animate()