import pygame
from settings.settings import *
from entity.entity import Entity
from utils.support import import_files
from random import choice

class Enemy(Entity):
    """Lớp chung cho các loại quái vật trên bản đồ.
    Có 4 loại quái vật: bamboo, raccoon, spirit và squid. """
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp, update_player_record, game_turn = 1):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.monster_name = monster_name
        self.update_player_record = update_player_record
        # Graphic Setup
        self.animations = self.import_graphics(monster_name)
        self.status = 'idle'
        [self.image, self.rect, self.hitbox] = self.generate_sprite(monster_name, pos)
        # Movement
        self.obstacle_sprites = obstacle_sprites
        # Stats
        self.bonus = 1
        self.generatate_basic_stats(monster_name, game_turn)
        # Player interaction
        self.init_player_interaction_stats(damage_player, trigger_death_particles, add_exp)
        # Sounds
        self.init_sfx()

    def init_player_interaction_stats(self, damage_player, trigger_death_particles, add_exp):
        """Khởi tạo các chỉ số liên quan đến việc tương tác với người chơi
        
        (method) init_player_interaction_stats(damage_player: function, trigger_death_particles: function, add_exp: function) -> None
        """
        self.can_atttack = True
        self.attack_time = None
        self.attack_cooldown = 1134
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        self.init_get_damage_timer()
        self.run_away = False

    def init_sfx(self):
        """Khởi tạo chỉ số về hiệu ứng âm thanh
        
        (method) init_sfx() -> None
        """
        self.death_sound = pygame.mixer.Sound('audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
        self.attack_sounnd = pygame.mixer.Sound(self.monster_info.get('attack_sound'))
        self.death_sound.set_volume(0.7)
        self.hit_sound.set_volume(0.7)
        self.attack_sounnd.set_volume(0.7)

    def init_get_damage_timer(self):
        """Khởi tạo chỉ số về thời gian có thể miễn giảm sát thương nhận vào
        
        (method) init_get_damage_timer() -> None
        """
        self.vulnerable = True
        self.get_hit_time = None
        self.invincibility_duration = 450

    def import_graphics(self, name):
        """Lấy các hoạt ảnh chuyển động của yêu quái
        
        (method) import_graphics(name: str) -> dict
        """
        animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/monsters/{name}/'
        for animation in animations.keys():
            animations[animation] = import_files(main_path + animation)
        return animations

    def generate_sprite(self, name, pos, inflate_info = [(20, -30), (0, -10)]):
        """Khởi tạo yêu quái thành một sprite trong game
        
        (method) import_graphics(name: str, pos: vec2, inflate_info: list) -> list
        """
        image = self.animations.get(self.status)[self.frame_idx]
        rect = image.get_rect(topleft = pos)
        hitbox = rect.inflate(inflate_info[0]) if name == 'raccoon' else rect.inflate(inflate_info[1])
        return [image, rect, hitbox]
    
    def generatate_basic_stats(self, name, game_turn):
        """Tạo các chỉ số cơ bản của yêu quái như tên, lượng máu, kinh nghiệm, tốc độ di chuyển,...
        
        (method) generatate_basic_stats(name: str, game_turn: int) -> None
        """
        # Monster get stronger after every new turn
        bonus_factor = 0.558 * pow(game_turn - 1, 2) + 0.358 * (game_turn - 1) + self.bonus 

        self.monster_name = name
        self.monster_info = monster_data[self.monster_name]
        self.health = self.monster_info.get('health') * bonus_factor
        self.exp = self.monster_info.get('exp') * bonus_factor
        self.speed = self.monster_info.get('speed')
        self.attack_damage = self.monster_info.get('damage') * bonus_factor
        self.resistance = self.monster_info.get('resistance')
        self.attack_radius = self.monster_info.get('attack_radius')
        self.notice_radius = self.monster_info.get('notice_radius')
        self.attack_type = self.monster_info.get('attack_type')

    def get_player_distance_direction(self, player):
        """Trả về khoảng cách và hướng để đi từ yêu quái đến người chơi
        
        (method) get_player_distance_direction(player: Player) -> dict
        """
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        direction = (player_vec - enemy_vec).normalize() if distance else pygame.math.Vector2((0, 0))
        return {'distance': distance, 'direction': direction}

    def set_status(self, player):
        """Cập nhật thông tin trạng thái hiện tại của yêu quái
        
        (method) get_status(player: Player) -> None
        """
        distance = self.get_player_distance_direction(player).get('distance')

        if distance <= self.attack_radius and self.can_atttack:
            if self.status != 'attack':
                self.frame_idx = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def action(self, player):
        """Thực hiện các hành động dựa trên trạng thái hiện tại của yêu quái
        
        (method) action(player: Player) -> None
        """
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks() if not self.attack_time else self.attack_time
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sounnd.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player).get('direction')
        else:
            self.direction = pygame.math.Vector2()

    def check_cooldowns(self):
        """Kiểm tra thời gian hồi của các chỉ số
        
        (method) check_cooldowns() -> None
        """
        current_time = pygame.time.get_ticks()

        if not self.can_atttack: 
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_atttack = True
                self.attack_time = None

        if not self.vulnerable:
            if current_time - self.get_hit_time >= self.invincibility_duration:
                self.vulnerable = True
                self.get_hit_time = None

    def animate(self):
        """Chạy hoạt ảnh của yêu quái dựa trên trạng thái
        
        (method) animate() -> None
        """
        animations = self.animations[self.status]
        self.frame_idx += self.animation_speed
        if self.frame_idx >= len(animations): 
            if self.status == 'attack':
                self.can_atttack = False
            self.frame_idx = 0

        self.image = animations[int(self.frame_idx)]
        self.rect = self.image.get_rect(center = self.hitbox.center) 
        # Flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_damage(self, player, attack_type):
        """Trừ máu của yêu quái nếu nhận phải sát thương từ người chơi
        
        (method) get_damage(player: Player, attack_type: str) -> None
        """
        if not self.vulnerable: return
        # Forwarding enemies direction to player after had been pushed back by Player Attack
        self.direction = self.set_random_run_away_direction(player)
        if attack_type == 'weapon':
            self.health -= player.calc_total_damage('weapon')
        else:
            self.health -= player.calc_total_damage('magic')
        self.get_hit_time = pygame.time.get_ticks()
        self.vulnerable = False
        self.hit_sound.play()

    def set_random_run_away_direction(self, player):
        """Xét hướng chạy ngẫu nhiên cho yêu quái nếu bị tấn công
        

        (method) set_random_run_away_direction(player: Player) -> str
        """
        run_direction = self.get_player_distance_direction(player).get('direction')
        if not self.run_away:
            run_away_prob = ['r', 'nr', 'r', 'nr', 'nr']
            direction = choice(run_away_prob)
            if direction == 'r':
                run_direction *= -1
                self.run_away = True
        return run_direction

    def check_death(self):
        """Kiểm tra nếu yêu quái đã chết hay chưa. Và chạy hoạt ảnh 'chết' nếu đã chết
        
        
        (method) check_death() -> None
        """
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.kill()
            self.add_exp(self.exp)
            self.death_sound.play()
            self.update_player_record(self.monster_name)
            
    def get_hit_reaction(self):
        """Giật yêu quái lùi theo hướng ngược lại với hướng di chuyển nếu bị tấn công
        
        (method) get_hit_reaction() -> None 
        """
        if not self.vulnerable:
            self.direction *= -self.resistance
    
    def update(self):
        self.get_hit_reaction()
        self.move(self.speed)
        self.animate()
        self.check_cooldowns()
        self.check_death()

    def enemy_update(self, player):
        """Hàm cập nhật yêu quái tùy chỉnh
        
        (method) enemy_update(player: Player) -> None 
        """
        self.set_status(player)
        self.action(player)