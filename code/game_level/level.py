import sys
import pygame
from attack.magic import MagicPlayer
from entity.player.animation_player import AnimationPlayer
from entity.enemy.enemy import Enemy
from utils.support import *
from settings.settings import TILESIZE
from game_level.tile import Tile
from entity.player.player import Player
from random import choice, randint
from attack.weapon import Weapon
from ui.ui import UI
from ui.item_upgrade import ItemUpgrade
from game_level.camera import YSortCameraGroup

class Level:
    """
        Lớp đại diện chứa các thông tin đến màn chơi. Bao gồm: bản đồ, hiển thị UI,
        chỉ số nhân vật, vũ khí người chơi, yêu quái,...
    """
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.is_game_over = False # game status
        self.game_is_started = False

        # Respawn enemy
        self.total_monster = []
        self.game_turn = 1
        self.new_turn_change_duration = 5000 # 5s before new wave of enemies coming
        self.end_turn_time = None

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Attack Sprite
        self.current_player_attack = None
        self.attack_sprites = pygame.sprite.Group() # player WEAPON attack 
        self.attackable_sprites = pygame.sprite.Group() # enemies ATTACKED by WEAPON

        # Sprite setup
        self.create_map()

        # User Interface
        self.ui = UI()
        self.upgrade = ItemUpgrade(self.player)

        # Particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # Monster killing history
        self.number_monster_killed = {'squid': 0, 'raccoon': 0, 'spirit': 0, 'bamboo': 0}

    def update_player_record(self, monster_name):
        """Cập nhật chỉ số quái vật đã tiêu diệt"""
        self.number_monster_killed[monster_name] += 1

    def respawn_monster(self):
        """Sinh ra một đợt quái vật mới khi người chơi đã tiêu diệt toàn bộ
        quái vật hiện có trên bản đồ"""
        self.game_turn += 1

        for _, monster_info in enumerate(self.total_monster):
            monster_name = monster_info[0]
            pos = monster_info[1]
            Enemy(
                monster_name,
                pos,
                [self.visible_sprites, self.attackable_sprites], 
                self.obstacle_sprites, 
                self.damage_player, 
                self.trigger_death_particle,
                self.add_exp,
                self.update_player_record,
                self.game_turn
            )
        
        self.end_turn_time = None

    def create_map(self):
        """ Khởi tạo bản đồ cho game. 
        Đối tượng khởi tạo bao gồm: biển, mặt đất, cỏ, cây, yêu quái, người chơi.
        """
        layouts = {
            'boundary': import_csv_file('map/map_FloorBlocks.csv'),
            'grass': import_csv_file('map/map_Grass.csv'),
            'large_object': import_csv_file('map/map_LargeObjects.csv'),
            'entities': import_csv_file('map/map_Entities.csv')
        }  
        graphics = {
            'grass': import_files('graphics/grass'),
            'large_object': import_files('graphics/objects')
        }
        # Lay ENEMIES and Objects
        for style, layout in layouts.items():
            for row_idx, row in enumerate(layout):
                for col_idx, col in enumerate(row):
                    if col != '-1':
                        x = col_idx * TILESIZE
                        y = row_idx * TILESIZE
                        pos = (x, y)
                        # Preventing Player from walking on the sea or running far away from the map
                        # and NOT displaying that hidden boundary
                        if style == 'boundary':
                            Tile(pos, [self.obstacle_sprites], 'invisible')
                        elif style == 'grass':
                            grass_imgs = graphics.get('grass')
                            img_surf_to_display = choice(grass_imgs)
                            Tile(
                                pos, 
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 
                                'grass', 
                                img_surf_to_display
                            )                                
                        elif style == 'large_object':
                            obj_surf = graphics.get('large_object')[int(col)]
                            Tile(pos, [self.visible_sprites, self.obstacle_sprites], 'large_object', obj_surf)
                        elif style == 'entities':
                            if col == '394':
                                # Init and Display Player
                                player_group = [self.visible_sprites]
                                # Add Player to visible groups and distinguish Player with the obstacle_sprites
                                self.player = Player(pos, player_group, self.obstacle_sprites, 
                                                            self.create_attack, self.destroy_attack, self.create_magic)            
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    pos,
                                    [self.visible_sprites, self.attackable_sprites], 
                                    self.obstacle_sprites, 
                                    self.damage_player, 
                                    self.trigger_death_particle,
                                    self.add_exp,
                                    self.update_player_record,
                                    self.game_turn
                                )
                                self.total_monster.append([monster_name, pos])

    def destroy_attack(self):
        """Hủy đòn đánh của người chơi"""
        if self.current_player_attack:
            self.current_player_attack.kill()
            self.current_player_attack = None

    def create_attack(self):
        """Tạo vũ khí cho người chơi"""
        self.current_player_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        """Tạo kĩ năng pháp thuật cho người chơi"""
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        elif style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
    
    def player_attack_logic(self):
        """
            Khởi tạo đòn tấn công và gây sát thương cho yêu quái
        """
        if not self.attack_sprites: return
        for attack_sprite in self.attack_sprites:
            # Check USER WEAPON collide with enemies 
            collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
            if collision_sprites:
                for target_sprite in collision_sprites:
                    sprite_type = target_sprite.sprite_type
                    if sprite_type == 'grass':
                        pos = target_sprite.rect.center
                        offset = pygame.math.Vector2(0, 44)
                        for leaf in range(randint(3, 6)):
                            self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                        target_sprite.kill()
                    else:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        """Giảm máu của người chơi nếu bị đánh trung và tạo hiệu ứng tương ứng"""
        if not self.player.vulnerable: return
        remains_health = self.player.health - amount
        self.player.health = remains_health if remains_health > 0 else 0
        self.player.vulnerable = False
        self.player.get_hurt_time = pygame.time.get_ticks()
        self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particle(self, pos, particle_type):
        """Tạo hiệu ứng trước khi chết của các quái vật"""
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_exp(self, amount):
        """Cộng kinh nghiệm cho người chơi"""
        self.player.exp += amount

    def toggle_menu(self):
        """Điều chỉnh trạng thái dừng/tiếp tục của game"""
        self.game_paused = not self.game_paused

    def dislay_ui(self):
        """Hiển thị các thông tin của người chơi và màn chơi lên màn hình"""
        self.ui.display(self.player)
        self.ui.display_player_record(self.number_monster_killed)
        self.ui.display_game_turn(self.game_turn)

    def run(self):
        """Theo dõi và cập nhật các sự kiện diễn ra trong vòng lặp của game"""
        self.visible_sprites.custom_draw(self.player)

        if self.player.health <= 0:
            self.game_paused = True

        if self.game_paused:
            if self.player.health > 0:
                self.upgrade.display()
                self.ui.show_exp(self.player.exp)
            else:
                self.ui.display_game_over_info()
                self.ui.display_restart_info()
                self.is_game_over = True
        elif not self.game_is_started:
            self.ui.display_game_menu()
            self.process_menu_options_input()
        else:
            self.dislay_ui()
            # Update Player direction
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
        
        # Respawn new wave of monsters if all monsters were killed 
        self.check_change_to_new_turn()

        return self.is_game_over
    
    def process_menu_options_input(self):
        """Xử lí input trên menu trước khi bắt đầu game"""
        keys = pygame.key.get_pressed()
        # Press Q to start game
        if keys[pygame.K_q]:
            self.game_is_started = True
        # Press ESC to quit game
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def check_change_to_new_turn(self):
        """Chuyển sang game sang vòng mới nếu đã hoàn thành màn chơi trước đó"""
        enemies_killed = sum(self.number_monster_killed.values())
        if enemies_killed == 35 * self.game_turn:
            self.end_turn_time = pygame.time.get_ticks() if self.end_turn_time is None else self.end_turn_time 
            current_time = pygame.time.get_ticks()
            if current_time - self.end_turn_time <= self.new_turn_change_duration:
                self.ui.display_change_to_new_turn()
            else:
                self.respawn_monster()