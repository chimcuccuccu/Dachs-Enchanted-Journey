import pygame
from demo_pygame.src.utilz.Config import DOOR_LAYER, BLACK, TILESIZE


class Door (pygame.sprite.Sprite):
    def __init__(self, game, x, y, scale_factor = 4):
        self.game = game
        self._layer = DOOR_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 16
        self.height = 16
        self.scale_factor = scale_factor

        self.image = self.game.door_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image,(self.width * self.scale_factor, self.height * self.scale_factor))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        pygame.mixer.init()
        self.door_open_sound = pygame.mixer.Sound('../../res/Ngan/sound_effects/door_opening.mp3')
        self.is_open = False

    def open(self):
        self.image = self.game.door_spritesheet.get_sprite(16, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image,(self.width * self.scale_factor, self.height * self.scale_factor))
        self.image.set_colorkey(BLACK)
        self.is_open = True

    def close(self):
        self.image = self.game.door_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * self.scale_factor, self.height * self.scale_factor))
        self.image.set_colorkey(BLACK)
        self.is_open = False

    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            if not self.is_open:
                self.door_open_sound.play()
                self.open()
        else:
            self.close()



