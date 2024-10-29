import pygame

from demo_pygame.src.utilz.config import *

class Thorn(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)  # Thêm gai vào all_sprites
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((34, 139, 34))  # Màu xanh lá cây tượng trưng cho gai
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = 'thorn'  # Đặt type là 'thorn' để nhận diện vũng gai