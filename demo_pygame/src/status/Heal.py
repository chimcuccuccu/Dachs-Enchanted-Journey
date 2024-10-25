import pygame

import math
from demo_pygame.src.utilz.config import *


class Heal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.heal
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE + 16

        self.animation_loop = 0

        self.image = self.game.heal_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y - TILESIZE // 2

    def update(self):
        self.animate()

    def animate(self):
        heal_animations = [self.game.heal_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(32, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(64, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(96, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(128, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(160, 0, self.width, self.height),]

        self.image = heal_animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.25
        if self.animation_loop >= 5:
            self.kill()