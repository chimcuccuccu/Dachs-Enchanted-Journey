import pygame

from demo_pygame.src.utilz.config import TILESIZE

class Fire(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)  # Thêm lửa vào all_sprites
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((255, 69, 0))  # Màu đỏ cam tượng trưng cho lửa
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = 'fire'  # Đặt type là 'fire' để nhận diện vũng lửa