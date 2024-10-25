import pygame

from demo_pygame.src.utilz.config import BLACK


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

        # Thêm phương thức get_size để lấy kích thước của sprite sheet
    def get_size(self):
        return self.sheet.get_size()  # Trả về kích thước của toàn bộ spritesheet