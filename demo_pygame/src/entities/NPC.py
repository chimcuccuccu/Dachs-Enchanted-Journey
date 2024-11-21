import pygame
from demo_pygame.src.utilz.Config import NPC_LAYER


class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, image_path):
        super().__init__()
        self._layer = NPC_LAYER
        self.game = game
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dialog = None  # Initialize dialog attribute

