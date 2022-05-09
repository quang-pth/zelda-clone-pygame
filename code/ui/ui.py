import pygame
from settings.settings import *

class UI:
    """Lớp giao diện chung cho cả game. 
    Hiển thị tất cả các thông tin, chỉ số liên quan lên màn hình.
    """
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Get all WEAPONS info
        self.weapon_graphics = self.get_equipment_surfs('weapon')
        # Get all MAGIC info
        self.magic_graphics = self.get_equipment_surfs('magic')
        # Game menu options
        self.menu_options = ['Press Q to start game', 'Press ESC to quit']
        
    # Show Health Point and Stamina
    def show_health_energy_bar(self, current_amount, max_amount, bg_rect, color):
        """Hiển thị thanh máu và năng lượng của người chơi lên góc trên trái màn hình"""
        # Draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        # Convert stat into pixel
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        # Drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        """Hiển thị lượng kinh nghiệm hiện tại của người chơi ở góc dưới phải màn hình"""
        text_surf = self.font.render("Exp:" + str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))
        # Drawing the player exp
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, can_switch_equiment):
        """Lấy rect hiển thị box vũ khí của người chơi"""
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        # Display box border when player clicks button to change weapon
        if not can_switch_equiment:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        
        return bg_rect

    def equip_overlay(self, type, idx, can_switch, left, top):
        """Hiển thị box vũ khí của người chơi ở góc trái dưới màn hình"""
        bg_rect = self.selection_box(left, top, can_switch)
        if type == 'weapon':
            surf_to_display = self.weapon_graphics[idx]
            # Display weapon change keyboard
            self.draw_equip_info("Q", left, top)
        else:
            surf_to_display = self.magic_graphics[idx]
            # Display magic change keyboard
            self.draw_equip_info("E", left, top)
        rect = surf_to_display.get_rect(center = bg_rect.center)
        self.display_surface.blit(surf_to_display, rect)
    
    def draw_equip_info(self, info_text, left, top):
        """Hiển thị phím tắt tương ứng với loại vũ khí của người chơi."""
        font_equip_info = pygame.font.Font(UI_FONT, 20)
        equip_info_surf = font_equip_info.render(info_text, False, TEXT_COLOR)
        equip_info_rect = equip_info_surf.get_rect(center = (left + 13, top + 10))
        self.display_surface.blit(equip_info_surf, equip_info_rect)

    def display(self, player):
        """Hiển thị thanh máu, năng lượng, vũ khí và các thông tin khác lên màn hình"""
        self.show_health_energy_bar(player.health, player.stats.get('health'), self.health_bar_rect, HEALTH_COLOR)
        self.show_health_energy_bar(player.energy, player.stats.get('energy'), self.energy_bar_rect, ENERGY_COLOR)
        self.equip_overlay('weapon', player.weapon_idx, player.can_switch_weapon, 10, HEIGTH - 100)
        self.equip_overlay('magic', player.magic_idx, player.can_switch_magic, 85, HEIGTH - 85)
    
    def display_game_over_info(self):
        """Hiển thị dòng chữ kết thúc game, nếu người chơi chết"""
        # GAME OVER text
        font_game_over = pygame.font.Font(UI_FONT, BIG_FONT_SIZE)
        game_over_text_surf = font_game_over.render("You die", False, TEXT_COLOR)
        game_over_text_rect = game_over_text_surf.get_rect(center = (WIDTH / 2, HEIGTH / 2))
        # Drawing the player exp
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, game_over_text_rect.inflate(20, 20))
        self.display_surface.blit(game_over_text_surf, game_over_text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, game_over_text_rect.inflate(20, 20), 3)

    def display_restart_info(self):
        """Hiển thị dòng chữ lựa chọn 'chơi lại hay không', nếu người chơi chết"""
        # RESTART GAME Text
        restart_game_text = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        restart_game_text_surf = restart_game_text.render("Press R to restart game", False, BLACK)
        offset = 100
        restart_game_text_rect = restart_game_text_surf.get_rect(center = (WIDTH / 2, HEIGTH / 2 + offset))
        # Drawing the player exp
        self.display_surface.blit(restart_game_text_surf, restart_game_text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, restart_game_text_rect.inflate(20, 20), 3)
    
    def display_player_record(self, number_monster_killed):
        """Hiển thị số lượng quái vật người chơi đã giết"""
        record_font = pygame.font.Font(UI_FONT, RECORD_FONT_SIZE)
        total_kills = sum(number_monster_killed.values())
        record_surf = record_font.render(f"Total Kills: {str(total_kills)}", False, BLACK)
        record_rect = record_surf.get_rect(bottomright = (WIDTH - 30, 40))
        # Drawing the player exp
        self.display_surface.blit(record_surf, record_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, record_rect.inflate(20, 20), 3)
    
    def display_game_turn(self, game_turn):
        """Hiển thị lượt đấu hiện tại của game"""
        record_font = pygame.font.Font(UI_FONT, RECORD_FONT_SIZE)
        record_surf = record_font.render(f"Round: {str(game_turn)}", False, BLACK)
        record_rect = record_surf.get_rect(center = (WIDTH / 2, 40))
        # Drawing the player exp
        self.display_surface.blit(record_surf, record_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, record_rect.inflate(20, 20), 3)
        
    def display_change_to_new_turn(self):
        """Hiển thị dòng chữ 'chuyển sang vòng đấu mới'"""
        font_game_over = pygame.font.Font(UI_FONT, 20)
        game_over_text_surf = font_game_over.render("5s before new turn of enemies", False, TEXT_COLOR)
        game_over_text_rect = game_over_text_surf.get_rect(center = (WIDTH / 2, HEIGTH / 2))
        # Drawing the player exp
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, game_over_text_rect.inflate(20, 20))
        self.display_surface.blit(game_over_text_surf, game_over_text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, game_over_text_rect.inflate(20, 20), 3)

    def display_game_menu(self):
        """Hiển thị menu khi bắt đầu game"""
        font_game_over = pygame.font.Font(UI_FONT, BIG_FONT_SIZE)
        game_over_text_surf = font_game_over.render("Zelda Clone", False, BLACK)
        game_over_text_rect = game_over_text_surf.get_rect(center = (WIDTH / 2, HEIGTH / 2 - 100))
        self.display_surface.blit(game_over_text_surf, game_over_text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, game_over_text_rect.inflate(20, 20), 3)
        self.display_menu_options()

    def display_menu_options(self):
        """Hiển thị các lựa chọn có trong menu bắt đầu game"""
        offset = 65
        font_game_over = pygame.font.Font(UI_FONT, 20)
        for idx in range(len(self.menu_options)):
            option = self.menu_options[idx]
            game_over_text_surf = font_game_over.render(option, False, BLACK)
            game_over_text_rect = game_over_text_surf.get_rect(center = (WIDTH / 2, HEIGTH / 2 + offset * (idx + 1)))
            self.display_surface.blit(game_over_text_surf, game_over_text_rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, game_over_text_rect.inflate(20, 20), 3)

    def get_equipment_surfs(self, type):
        """Lấy hình ảnh của các loại vữ khí và phép thuật"""
        graphics = []
        if type == 'weapon':
            graphic_to_use = weapon_data.values()
        else:
            graphic_to_use = magic_data.values()
        for equip_info in graphic_to_use:
            path = equip_info['graphic']
            equip_info = pygame.image.load(path).convert_alpha()
            graphics.append(equip_info)
        return graphics