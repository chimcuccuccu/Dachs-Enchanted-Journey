import pygame
from demo_pygame.src.utilz.config import *

class Generic (pygame.sprite.Sprite):
    def __init__(self, game, pos, surf, groups, z = GROUND_LAYER):
        self.game = game
        self.groups = self.game.all_sprites
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self._layer = z