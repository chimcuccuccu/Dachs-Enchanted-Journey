import pygame

from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        # self.sheet = pygame.image.load(file).convert()
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        # sprite = pygame.Surface(([width, height]))
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

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

        # image_to_load = pygame.image.load("img/single2.png")
        # self.image = pygame.Surface([self.width , self.height])
        # self.image.set_colorkey(BLACK)
        # self.image.blit(image_to_load, (0, 0))
        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                # if self.y_change > 0:
                # if self.y_change < 0:

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        # info = pygame.display.Info()
        #
        # screen_width = info.current_w
        # screen_height = info.current_h
        # width_rate = screen_width / 640
        # height_rate = screen_width / 500
        # self.width *= width_rate
        # self.height *= height_rate
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


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # self.image = pygame.Surface([self.width, self.height])
        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)
        # self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h
        self.game = game
        self._layer = GROUD_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # self.width = screen_width
        # self.height = screen_height
        self.image = pygame.image.load('img/Map1.png').convert_alpha()
        # self.image = self.game.nganMapSprite()

        self.rect = self.image.get_rect()
        # self.rect.x = self.x
        # self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('Arialn.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.fg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.bg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

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



