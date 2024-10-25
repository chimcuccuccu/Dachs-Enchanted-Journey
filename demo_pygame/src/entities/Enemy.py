import random

import pygame
import math

from demo_pygame.src.utilz.config import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        # Tính khoảng cách giữa player và enemy
        distance = math.sqrt(
            (self.game.player.rect.x - self.rect.x) ** 2 + (self.game.player.rect.y - self.rect.y) ** 2)

        # Nếu khoảng cách giữa enemy và player nhỏ hơn 200 pixel thì bám đuổi player
        if distance < 200:
            dx = self.game.player.rect.x - self.rect.x
            dy = self.game.player.rect.y - self.rect.y

            # Xác định ưu tiên hướng di chuyển
            if abs(dx) > abs(dy):  # Di chuyển theo chiều ngang
                if dx > 0:
                    self.x_change = ENEMY_SPEED
                    self.facing = 'right'
                else:
                    self.x_change = -ENEMY_SPEED
                    self.facing = 'left'
                self.y_change = 0  # Chỉ di chuyển theo trục x
            else:  # Di chuyển theo chiều dọc
                if dy > 0:
                    self.y_change = ENEMY_SPEED
                    self.facing = 'down'
                else:
                    self.y_change = -ENEMY_SPEED
                    self.facing = 'up'
                self.x_change = 0  # Chỉ di chuyển theo trục y
        else:
            # Nếu không trong phạm vi, tiếp tục di chuyển như bình thường
            if self.facing == 'left':
                self.x_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = 'right'

            if self.facing == 'right':
                self.x_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = 'left'
            if self.facing == 'up':
                self.y_change -= ENEMY_SPEED
            if self.facing == 'down':
                self.y_change += ENEMY_SPEED

        # Sau khi cập nhật hướng, ta sẽ gọi lại hàm animate để đảm bảo đúng hoạt ảnh

    def animate(self):

        down_animations = [self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(64, 0, self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(64, 32, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(64, 64, self.width, self.height)]

        up_animations = [self.game.enemy_spritesheet.get_sprite(0, 96, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(32, 96, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(64, 96, self.width, self.height)]

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

