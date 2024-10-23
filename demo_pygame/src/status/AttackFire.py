import pygame
import math

from BTL_Python_Nhom7.demo_pygame.src.utilz.config import *


class AttackFire(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacksFire
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.direction = direction
        self.animation_loop = 0

        self.image = self.game.attackFire_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()
        self.move()

        if self.rect.right < 0 or self.rect.left > self.game.screen.get_width() or \
                self.rect.bottom < 0 or self.rect.top > self.game.screen.get_height():
            self.kill()

    def collide(self):
         hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        # direction = self.game.player.facing

        right_animations = [self.game.attackFire_spritesheet.get_sprite(0, 48, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(48, 48, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(96, 48, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(144, 48, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(192, 48, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(240, 48, self.width + 16, self.height + 16),]

        left_animations = [self.game.attackFire_spritesheet.get_sprite(0, 0, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(48, 0, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(96, 0, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(144, 0, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(192, 0, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(240, 0, self.width + 16, self.height + 16),]

        up_animations = [self.game.attackFire_spritesheet.get_sprite(0, 144, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(48, 144, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(96, 144, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(144, 144, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(192, 144, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(240, 144, self.width + 16, self.height + 16),]

        down_animations = [self.game.attackFire_spritesheet.get_sprite(0, 96, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(48, 96, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(96, 96, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(144, 96, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(192, 96, self.width + 16, self.height + 16),
                            self.game.attackFire_spritesheet.get_sprite(240, 96, self.width + 16, self.height + 16),]

        if self.direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.6
            if self.animation_loop >= 6:
                self.animation_loop = 0

        if self.direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.6
            if self.animation_loop >= 6:
                self.animation_loop = 0

        if self.direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.6
            if self.animation_loop >= 6:
                self.animation_loop = 0

        if self.direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.6
            if self.animation_loop >= 6:
                self.animation_loop = 0

    def move(self):
        speed = 3

        if self.direction == 'up':
            self.rect.y -= speed
        elif self.direction == 'down':
            self.rect.y += speed
        elif self.direction == 'left':
            self.rect.x -= speed
        elif self.direction == 'right':
            self.rect.x += speed