import pygame, sys
from code import *
from game_level.level import Level
from settings.settings import *

class Game:
	"""Lớp chính của game. 
	Chứa toàn bộ các thông tin liên quan và vòng lặp của game"""
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
		pygame.display.set_caption('Zelda Clone')
		self.clock = pygame.time.Clock()
		self.level = Level()
		# Main sound
		self.main_sound = pygame.mixer.Sound('audio/main.ogg')
		self.main_sound.set_volume(0.68)
		self.main_sound.play(loops = -1)
		self.game_is_over = False

	def run(self):
		"""Khởi chạy game và xử lí các input liên quan"""
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()
					# Press R to restart new game if game was over
					if self.game_is_over and event.key == pygame.K_r:
						self.level = Level()

			self.screen.fill(WATER_COLOR)
			
			self.game_is_over = self.level.run()
			
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()