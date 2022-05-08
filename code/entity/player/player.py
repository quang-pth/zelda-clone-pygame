import pygame
from entity.entity import Entity
from settings.settings import *
from utils.support import import_files

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.sprite_type = 'player'
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET.get('player'))
        # Animations Setupl
        self.import_player_assets()
        # Movement Init
        self.status = 'down'
        # Attack Attr Init
        self.init_attack_attr(create_attack, destroy_attack)
        # Magic
        self.init_magic_attr(create_magic)
        # Stats
        self.init_stats()
        # Enemies
        self.obstacle_sprites = obstacle_sprites
        # Damage timer
        self.vulnerable = True
        self.get_hurt_time = None
        self.invulnerability_duration = 500
        # Sounds
        self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)
    
    def init_attack_attr(self, create_attack, destroy_attack):
        # Attacking
        self.attacking = False
        self.base_cooldown = 400
        self.attack_time = None
        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_idx = 0
        self.weapons = list(weapon_data.keys()) 
        self.using_weapon = self.weapons[self.weapon_idx]
        self.weapon_cooldown = weapon_data.get(self.using_weapon).get('cooldown')
        # CHANGE weapon timer
        self.can_switch_weapon = True
        self.switch_duration_cooldown = 300
        self.weapon_switch_time = None
    
    def init_magic_attr(self, create_magic):
        self.create_magic = create_magic
        self.magic_idx = 0
        self.magics = list(magic_data.keys()) 
        self.using_magic = self.magics[self.magic_idx]
        self.can_switch_magic = True
        self.magic_switch_time = None

    def init_stats(self):
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats.get('health') * 0.5
        self.energy = self.stats.get('energy') * 0.8
        self.speed = self.stats.get('speed')
        self.exp = 0

    def import_player_assets(self):
        character_path = 'graphics/player'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [], 
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': [],
        }
        for animation in self.animations.keys():
            # Get full animation path
            animation_full_path = character_path + "/" + animation
            # Import animation states
            self.animations[animation] = import_files(animation_full_path)
        
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            # Movement Input
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            # Stop if user lifts up the key
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            # Stop if user lifts up the key
            else:
                self.direction.x = 0

            # Attack Input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            # Magic Input
            elif keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                # Get USING MAGIC info
                magic_style = self.using_magic
                magic_strength = magic_data[self.using_magic].get('strength') + self.stats.get('magic')
                magic_cost = magic_data[self.using_magic].get('cost')
                self.create_magic(magic_style, magic_strength, magic_cost)
        # Change Weapon
        if self.can_switch_weapon:
            if keys[pygame.K_q]:
                # Set Cooldown for chaning weapon
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                # Update Player using weapon
                self.weapon_idx += 1
                if self.weapon_idx >= len(self.weapons):
                    self.weapon_idx = 0
                self.using_weapon = self.weapons[self.weapon_idx]
        # Change Magic
        if self.can_switch_magic:
            if keys[pygame.K_e]:
                # Set Cooldown for chaning weapon
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                # Update Player using weapon
                self.magic_idx += 1
                if self.magic_idx >= len(self.magics):
                    self.magic_idx = 0
                self.using_magic = self.magics[self.magic_idx]
        
    def get_status(self):
        # IDLE status
        if self.direction.x == 0 and self.direction.y == 0 and not self.attacking:
            if not 'idle' in self.status and not 'attack' in self.status: 
                self.status += "_idle"
        # Player can not attacking while moving
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace("idle", "attack")
                else:
                    self.status += "_attack"
        else:
            self.status = self.status.removesuffix("_attack")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.base_cooldown + self.weapon_cooldown:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        if not self.vulnerable:
            if current_time - self.get_hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
                
    def animate(self):
        animation = self.animations[self.status]
        # Loop over the frame idx
        self.frame_idx += self.animation_speed
        if self.frame_idx >= len(animation):
            self.frame_idx = 0
        # Update player animation
        self.image = animation[int(self.frame_idx)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        # Flicker
        if not self.vulnerable:
            value = self.wave_value()
            self.image.set_alpha(value)
        else:
            self.image.set_alpha(255)
    
    def get_full_damage(self, type):
        if type == 'weapon': # physical weapon
            base_damage = self.stats.get('attack')
            bonus_damage = weapon_data.get(self.using_weapon).get('damage')
        else: # magic 
            base_damage = self.stats.get('magic')
            bonus_damage = magic_data.get(self.using_magic).get('strength')
        return base_damage + bonus_damage

    def energy_recovery(self):
        energy_after_recover = self.energy + 0.0333 * self.stats.get('magic') 
        max_energy = self.stats.get('energy')
        if energy_after_recover < max_energy:
            self.energy = energy_after_recover
        else:
            self.energy = max_energy

    def get_value_by_idx(self, idx):
        return list(self.stats.values())[idx]

    def get_cost_by_idx(self, idx):
        return list(self.upgrade_cost.values())[idx]

    def update(self):
        self.input()
        self.move(self.stats.get('speed'))
        self.get_status()
        self.animate()
        self.cooldowns()
        self.energy_recovery()