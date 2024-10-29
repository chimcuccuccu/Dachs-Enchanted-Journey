import pygame

from demo_pygame.src.utilz.config import TILESIZE

class IcePatch(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)  # Thêm ice vào all_sprites
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((173, 216, 230))  # Màu xanh nhạt tượng trưng cho băng
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = 'ice'  # Đặt type là 'ice' để nhận diện vũng băng
