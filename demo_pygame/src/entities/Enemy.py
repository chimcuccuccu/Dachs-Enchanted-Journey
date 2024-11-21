import random
import pygame
import math

from demo_pygame.src.utilz.Config import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, scale=2):
        self.scale = scale
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

    def destroy(self):
        self.kill()

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0


    def movement(self):
        # Calculate the distance between the player and the enemy
        distance = math.sqrt(
            (self.game.player.rect.x - self.rect.x) ** 2 + (self.game.player.rect.y - self.rect.y) ** 2)

        # If the distance between the enemy and the player is less than 200 pixels, chase the player
        if distance < 200:
            dx = self.game.player.rect.x - self.rect.x
            dy = self.game.player.rect.y - self.rect.y

            # Determine the priority direction of movement
            if abs(dx) > abs(dy):  # Move horizontally
                if dx > 0:
                    new_x = self.rect.x + ENEMY_SPEED
                    if not self.collides_with_objects(new_x, self.rect.y):
                        self.x_change = ENEMY_SPEED
                        self.facing = 'right'
                else:
                    new_x = self.rect.x - ENEMY_SPEED
                    if not self.collides_with_objects(new_x, self.rect.y):
                        self.x_change = -ENEMY_SPEED
                        self.facing = 'left'
                self.y_change = 0  # Only move along the x-axis
            else:  # Move vertically
                if dy > 0:
                    new_y = self.rect.y + ENEMY_SPEED
                    if not self.collides_with_objects(self.rect.x, new_y):
                        self.y_change = ENEMY_SPEED
                        self.facing = 'down'
                else:
                    new_y = self.rect.y - ENEMY_SPEED
                    if not self.collides_with_objects(self.rect.x, new_y):
                        self.y_change = -ENEMY_SPEED
                        self.facing = 'up'
                self.x_change = 0  # Only move along the y-axis
        else:
            # If not in range, continue moving as usual
            if self.facing == 'left':
                new_x = self.rect.x - ENEMY_SPEED
                if not self.collides_with_objects(new_x, self.rect.y):
                    self.x_change -= ENEMY_SPEED
                    self.movement_loop -= 1
                    if self.movement_loop <= -self.max_travel:
                        self.facing = 'right'

            if self.facing == 'right':
                new_x = self.rect.x + ENEMY_SPEED
                if not self.collides_with_objects(new_x, self.rect.y):
                    self.x_change += ENEMY_SPEED
                    self.movement_loop += 1
                    if self.movement_loop >= self.max_travel:
                        self.facing = 'left'
            if self.facing == 'up':
                new_y = self.rect.y - ENEMY_SPEED
                if not self.collides_with_objects(self.rect.x, new_y):
                    self.y_change -= ENEMY_SPEED
            if self.facing == 'down':
                new_y = self.rect.y + ENEMY_SPEED
                if not self.collides_with_objects(self.rect.x, new_y):
                    self.y_change += ENEMY_SPEED

    #check va cham giua enemies va object
    def collides_with_objects(self, x, y):
        temp_rect = self.rect.copy()
        temp_rect.x = x
        temp_rect.y = y
        for obj in self.game.collidables:
            if temp_rect.colliderect(obj.rect):
                return True
        return False

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
                self.image = down_animations[0]
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = up_animations[0]
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = right_animations[0]
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = left_animations[0]
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1