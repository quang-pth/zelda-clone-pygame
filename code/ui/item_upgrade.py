import pygame
from settings.settings import *
from ui.item import Item

class ItemUpgrade:
    def __init__(self, player):        
        self.display_surf = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(self.player.stats)
        self.attribute_names = list(self.player.stats.keys())
        self.max_value = list(self.player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        # Items
        self.height = self.display_surf.get_size()[1] * 0.8
        self.width = self.display_surf.get_size()[0] // 6
        self.create_items()
        # Selection System
        self.selection_idx = 0
        self.selection_time = None
        self.can_move = True 
        self.disable_duration = 199

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.move_indicator('right')
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.move_indicator('left')
            
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_idx].trigger(self.player)
    
    def move_indicator(self, direction):
        if direction == 'right':
            self.selection_idx += 1
            if self.selection_idx >= self.attribute_nr:
                self.selection_idx = 0
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        else:
            self.selection_idx -= 1
            if self.selection_idx < 0:
                self.selection_idx = self.attribute_nr - 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()

    def create_items(self): 
        self.item_list = []

        for idx, item in enumerate(range(self.attribute_nr)):
            # Horizontal position
            full_width = self.display_surf.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2 

            # Vertical position
            top = self.display_surf.get_size()[1] * 0.1 

            # Create the object
            item = Item(left, top, self.width, self.height, idx, self.font)
            self.item_list.append(item)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= self.disable_duration:
                self.can_move = True

    def display(self):
        self.input()
        self.selection_cooldown()
        # Draw all items
        for idx, item in enumerate(self.item_list):
            # Get attributes
            name = self.attribute_names[idx]
            value = self.player.get_value_by_idx(idx)
            max_value = self.max_value[idx]
            cost = self.player.get_cost_by_idx(idx)
            item.display(self.display_surf, self.selection_idx, name, value, max_value, cost)