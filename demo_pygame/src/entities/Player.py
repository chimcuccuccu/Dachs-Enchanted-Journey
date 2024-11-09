import pygame
import math

from demo_pygame.src.status.Attack import Attack
from demo_pygame.src.status.AttackFire import AttackFire
from demo_pygame.src.status.Heal import Heal
from demo_pygame.src.utilz.Config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, scale_factor=1.3):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        self.scale_factor = scale_factor
        pygame.sprite.Sprite.__init__(self, self.groups)
        # super().__init__(self.groups)

        self.x = x
        self.y = y
        info = pygame.display.Info()

        # Thiết lập kích thước và vị trí
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        # Tải hình ảnh ban đầu cho người chơi
        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_coin()
        self.collide_enemy()

        # Cập nhật vị trí người chơi
        self.rect.x += self.x_change
        for collidable in self.game.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.x_change > 0:  # Moving right
                    self.rect.right = collidable.rect.left
                elif self.x_change < 0:  # Moving left
                    self.rect.left = collidable.rect.right
                break  # Stop checking further for efficiency

        self.rect.y += self.y_change
        for collidable in self.game.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.y_change > 0:  # Moving down
                    self.rect.bottom = collidable.rect.top
                elif self.y_change < 0:  # Moving up
                    self.rect.top = collidable.rect.bottom
                break  # Stop checking further for efficiency

        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        for collidable in self.game.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.x_change > 0:  # Moving right
                    self.rect.right = collidable.rect.left
                elif self.x_change < 0:  # Moving left
                    self.rect.left = collidable.rect.right
                break  # Stop checking further for efficiency

        self.rect.y += self.y_change
        for collidable in self.game.collidables:
            if self.rect.colliderect(collidable.rect):
                if self.y_change > 0:  # Moving down
                    self.rect.bottom = collidable.rect.top
                elif self.y_change < 0:  # Moving up
                    self.rect.top = collidable.rect.bottom
                break  # Stop checking further for efficiency

        # Đặt lại thay đổi để tránh lặp vô hạn
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.x_change -= PLAYER_SPEED
                self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            if self.rect.right < self.game.map_width:
                self.x_change += PLAYER_SPEED
                self.facing = 'right'
        if keys[pygame.K_UP]:
            if self.rect.top > 0:
                self.y_change -= PLAYER_SPEED
                self.facing = 'up'
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < self.game.map_height:
                self.y_change += PLAYER_SPEED
                self.facing = 'down'

    def collide_enemy(self):
        # Kiểm tra va chạm với kẻ thù
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        if hits:
            self.kill()  # Xóa người chơi khỏi nhóm sprite
            self.game.playing = False  # Dừng trò chơi

    def collide_coin(self):
        # Kiểm tra va chạm với đồng xu
        hits = pygame.sprite.spritecollide(self, self.game.coins, True)  # Xóa đồng xu khi va chạm
        if hits:
            # Cộng điểm cho mỗi đồng xu thu thập được
            self.game.score += len(hits)


    def animate(self):
        # Các ảnh động dựa trên hướng di chuyển
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

        self.image = pygame.transform.scale(self.image, (self.width * self.scale_factor, self.height * self.scale_factor))

