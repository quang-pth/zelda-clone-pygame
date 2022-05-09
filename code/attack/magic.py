import pygame
from settings.settings import *

class MagicPlayer:
    """Lớp chứa thông tin về các đòn tấn công bằng phép thuật.
    Có 2 loại phép thuật: hồi máu và chưởng lửa"""
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('audio/heal.wav'),
            'flame': pygame.mixer.Sound('audio/Fire.wav'),
        }
    
    def heal(self, player, strength, cost, groups):
        """Sử dụng phép hồi máu. 
        Hồi máu cho người chơi và tạo hiệu ứng hồi máu"""
        if player.energy < cost: return        
        
        self.sounds.get('heal').play()
        health_after_heal = player.health + strength
        max_health = player.stats.get('health')
        # Healing shouldn't be applied when exceeding player maximum health
        if health_after_heal >= max_health:
            player.health = player.stats.get('health')
        else: 
            player.health = health_after_heal
        player.energy -= cost
        # Display particle effect
        offset = pygame.math.Vector2(0, -60)
        self.animation_player.create_particles('aura', player.rect.center, groups)
        self.animation_player.create_particles('heal', player.rect.center + offset, groups)

    def flame(self, player, cost, groups):
        """Sử dụng phép chưởng lửa. 
        Tấn công, đẩy lùi mục tiêu và tạo hiệu ứng lửa"""
        if player.energy < cost: return

        self.sounds.get('flame').play()
        player.energy -= cost
        player_direction = player.status.split('_')[0]
        if player_direction == 'right':
            spell_direction = pygame.math.Vector2(1, 0)
        elif player_direction == 'left':
            spell_direction = pygame.math.Vector2(-1, 0)
        elif player_direction == 'up':
            spell_direction = pygame.math.Vector2(0, -1)
        else: # down
            spell_direction = pygame.math.Vector2(0, 1)
        # We have 5 frames of Flame animation
        for i in range(1, 6):
            if spell_direction.x: 
                offset_x = spell_direction.x * i * TILESIZE
                animate_pos = player.rect.center + pygame.math.Vector2(offset_x, 0)
                self.animation_player.create_particles('flame', animate_pos, groups)
            else:
                offset_y = spell_direction.y * i * TILESIZE
                animate_pos = player.rect.center + pygame.math.Vector2(0, offset_y)
                self.animation_player.create_particles('flame', animate_pos, groups)