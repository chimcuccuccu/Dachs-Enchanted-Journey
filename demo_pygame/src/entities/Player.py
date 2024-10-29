import pygame
import math

from demo_pygame.src.status.Collide import Collide
from demo_pygame.src.utilz.config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        # super().__init__(self.groups)

        self.x = x
        self.y = y
        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        # Thêm thuộc tính máu cho nhân vật
        self.health = 100  # Máu hiện tại
        self.max_health = 200  # Máu tối đa
        self.speed = PLAYER_SPEED


        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.collide = Collide(self)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide.collide_enemy()
        self.collide.Collide_bleeding()
        self.collide.Collide_ice()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.groups:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.groups:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.groups:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.groups:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'


    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 32, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(64, 64, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(0, 96, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(32, 96, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(64, 96, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 96, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
