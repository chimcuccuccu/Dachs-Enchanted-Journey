import random
import pygame
from demo_pygame.src.entities.Enemy import Enemy
from demo_pygame.src.utilz.config import *

class EnemySpawner:
    def __init__(self, game, map_image):
        self.game = game
        self.map_image = map_image

    def spawn_random_enemies(self, number_of_enemies):
        tile_size = TILESIZE  # Kích thước mỗi tile (điều chỉnh theo kích thước thực tế của map)
        map_width, map_height = self.map_image.get_size()

        # Danh sách lưu các vị trí đã chọn để tránh spawn trùng
        chosen_positions = []

        for _ in range(number_of_enemies):
            while True:
                # Chọn vị trí ngẫu nhiên
                x = random.randint(0, map_width // tile_size - 1)
                y = random.randint(0, map_height // tile_size - 1)

                # Kiểm tra xem vị trí này đã chọn chưa, nếu chưa thì thêm vào danh sách
                if (x, y) not in chosen_positions:
                    chosen_positions.append((x, y))
                    # Tạo enemy ở vị trí (x, y)
                    Enemy(self.game, x, y)
                    break
