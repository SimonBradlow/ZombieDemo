import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, row, frame, width, height, scale):
		image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), (row * height), width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))

		return image
