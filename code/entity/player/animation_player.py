from utils.support import import_files
from random import choice
from particle_effect.particle import ParticleEffect
import pygame

class Animation:
	"""Lớp xử lí các hoạt ảnh cho game.
	Các hoạt ảnh bao gồm: hoạt ảnh di chuyển của người chơi, yêu quái, hiệu ứng pháp thuật,...
	"""
	
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
		"""Lật ảnh
        
        (method) reflect_images(frames: list) -> list 
        """
		new_frames = []
		for frame in frames:
			flipped_frame = pygame.transform.flip(frame, True, False)
			new_frames.append(flipped_frame)
		return new_frames
	
	def create_grass_particles(self, pos, groups):
		"""Tạo hiệu ứng của cỏ
        
        (method) create_grass_particles(pos: vec2, groups: list) -> None 
        """
		animation_frames = choice(self.frames['leaf'])
		ParticleEffect(pos, animation_frames, groups)
	
	def create_particles(self, animation_type, pos, groups):
		"""Tạo hiệu ứng tương ứng với animation_type
        
        (method) create_particles(animation_type: str, pos: vec2, groups: list) -> None 
        """
		animation_frames = self.frames.get(animation_type)
		ParticleEffect(pos, animation_frames, groups)