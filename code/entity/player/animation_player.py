from utils.support import import_files
from random import choice
from particle_effect.particle import ParticleEffect
import pygame

class AnimationPlayer:
    def __init__(self):
        self.frames = {
			# magic
			'flame': import_files('graphics/particles/flame/frames'),
			'aura': import_files('graphics/particles/aura'),
			'heal': import_files('graphics/particles/heal/frames'),
			
			# attacks 
			'claw': import_files('graphics/particles/claw'),
			'slash': import_files('graphics/particles/slash'),
			'sparkle': import_files('graphics/particles/sparkle'),
			'leaf_attack': import_files('graphics/particles/leaf_attack'),
			'thunder': import_files('graphics/particles/thunder'),

			# monster deaths
			'squid': import_files('graphics/particles/smoke_orange'),
			'raccoon': import_files('graphics/particles/raccoon'),
			'spirit': import_files('graphics/particles/nova'),
			'bamboo': import_files('graphics/particles/bamboo'),
			
			# leafs 
			'leaf': (
				import_files('graphics/particles/leaf1'),
				import_files('graphics/particles/leaf2'),
				import_files('graphics/particles/leaf3'),
				import_files('graphics/particles/leaf4'),
				import_files('graphics/particles/leaf5'),
				import_files('graphics/particles/leaf6'),
				self.reflect_images(import_files('graphics/particles/leaf1')),
				self.reflect_images(import_files('graphics/particles/leaf2')),
				self.reflect_images(import_files('graphics/particles/leaf3')),
				self.reflect_images(import_files('graphics/particles/leaf4')),
				self.reflect_images(import_files('graphics/particles/leaf5')),
				self.reflect_images(import_files('graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)
    
    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames.get(animation_type)
        ParticleEffect(pos, animation_frames, groups)