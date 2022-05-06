# Game Window default setup
SCENE_RATIO = 3 / 5
WIDTH    = 1920 * SCENE_RATIO
HEIGTH   = 1080 * SCENE_RATIO
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
        'player': -26,
        'large_object': -40,
        'grass': -10,
        'invisible': 0,
}

# General Colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
BLACK = '#111111'
RECORD_FONT_SIZE = 17

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
BIG_FONT_SIZE = 100
# UI COLOR
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# Upgrade Menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# Player WEAPON
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 35, 'graphic': 'graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': 'graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': 'graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': 'graphics/weapons/sai/full.png'},
}

# Magio
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': 'graphics/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': 'graphics/particles/heal/heal.png'},
}

# Enimes
# resistance: distance is pushed back when attacked by the Player
monster_data = {
    'squid': {'health': 100, 'exp': 100, 'damage': 25, 'attack_type': 'slash', 'attack_sound': 'audio/attack/slash.wav',
            'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 400, 'exp': 250, 'damage': 40, 'attack_type': 'claw', 'attack_sound': 'audio/attack/claw.wav', 
            'speed': 2, 'resistance': 4, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100, 'exp': 110, 'damage': 23, 'attack_type': 'thunder', 'attack_sound': 'audio/attack/fireball.wav', 
            'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70, 'exp': 120, 'damage': 14, 'attack_type': 'leaf_attack', 'attack_sound': 'audio/attack/slash.wav', 
            'speed': 3, 'resistance': 2, 'attack_radius': 50, 'notice_radius': 300},
}