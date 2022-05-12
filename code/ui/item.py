import pygame
from settings.settings import *

class Item:
    """Lớp biểu diễn cho từng chỉ số nâng cấp được hiển thị trên màn hình.
    Thông tin bao gồm: idx của chỉ số, font chữ, màu sắc,...
    """
    def __init__(self, left, top, width, height, idx, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.idx = idx
        self.font = font
    
    def display_name(self, surface, name, cost, selected):
        """Hiển thị tên của chỉ số lên màn hình.
        Màu chữ sẽ thay đổi theo nếu thông số đó đang được chọn.
        
        (method) display_name(surface: Surface, name: str, cost: float, selected: bool) -> None
        """
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # Title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))
        # Cost
        cost_surf = self.font.render(f'Cost: {int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0, -20))

        # Draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        """Hiển thị thanh bar đại diện cho mức nâng cấp hiện tại của mỗi thông số.
        
        (method) display_bar(surface: Surface, value: int, max_value: int, selected: bool) -> None
        """
        # setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0, -60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        pygame.draw.line(surface, color, top, bottom, 5) 
        # Bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        """Nâng cấp chỉ số nếu thỏa điều kiện
        
        (method) trigger(player: Player) -> None
        """
        upgrade_attr = list(player.stats.keys())[self.idx]
        
        if player.exp >= player.upgrade_cost[upgrade_attr] and player.stats[upgrade_attr] < player.max_stats[upgrade_attr]:
            player.exp -= player.upgrade_cost[upgrade_attr]
            stat_after_upgrade = player.stats[upgrade_attr] * 1.2
            if stat_after_upgrade >  player.max_stats[upgrade_attr]:
                player.stats[upgrade_attr] = player.max_stats[upgrade_attr]
            else:
                player.stats[upgrade_attr] = stat_after_upgrade

            player.upgrade_cost[upgrade_attr] *= 1.4

    def display(self, surface, selection_num, name, value, max_value, cost):
        """Hiển thị thông số lên màn hình
        
        (method) display(surface: Surface, selection_num: int, name: str, value: int, max_value: int, cost: float) -> None
        """
        is_selected = self.idx == selection_num

        if is_selected:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)

        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 5)
        self.display_name(surface, name, cost, is_selected)
        self.display_bar(surface, value, max_value, is_selected)