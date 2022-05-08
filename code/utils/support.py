    from csv import reader
from os import walk
import pygame

def import_csv_file(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(row)
        return terrain_map

def import_files(path):
    surface_list = []
    # Extract file path, subfolder path and subfile path
    for _, __, img_files in walk(path):
        for img_path in img_files:
            full_path = path + '/' + img_path 
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list