import pygame

from demo_pygame.src.utilz.Config import TREE_LAYER, TILESIZE


class Objects (pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, image_path, scale_factor = 3, load_image = True):
        self.game = game
        self._layer = TREE_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = width * scale_factor
        self.height = height * scale_factor

        if load_image and image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((0, 0, 0, 0))  # Fill with a color for visibility
            self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.setPosition()

    def setPosition(self):
        # print(f"Player y: {self.game.player.rect.y}, Tree y: {self.rect.y}")
        if self.game.player.rect.y > self.rect.y + self.height:
            self._layer = self.game.player._layer - 1
        else:
            self._layer = 20