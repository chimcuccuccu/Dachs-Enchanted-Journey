import pygame
import random
from demo_pygame.src.entities.Coin import Coin
from demo_pygame.src.utilz.Config import *

class CoinSpawner:
    def __init__(self, game, map_image):
        self.game = game  # Tham chiếu đến đối tượng trò chơi chính
        self.map_image = map_image  # Hình ảnh bản đồ để xác định kích thước
        self.last_spawn_time = pygame.time.get_ticks()  # Thời gian spawn coin gần nhất

    def spawn_random_coins(self, number_of_coins=20):
        """Hàm spawn ngẫu nhiên số lượng coin chỉ định lên bản đồ."""
        tile_size = TILESIZE  # Kích thước mỗi tile
        map_width, map_height = self.map_image.get_size()  # Lấy kích thước bản đồ

        # Danh sách lưu các vị trí đã chọn để tránh spawn trùng
        chosen_positions = []

        for _ in range(number_of_coins):
            while True:
                # Chọn vị trí ngẫu nhiên
                x = random.randint(0, map_width // tile_size - 1)
                y = random.randint(0, map_height // tile_size - 1)

                # Kiểm tra xem vị trí này đã được chọn chưa
                if (x, y) not in chosen_positions:
                    chosen_positions.append((x, y))  # Thêm vị trí vào danh sách đã chọn
                    # Tạo coin ở vị trí (x, y) và thêm vào game
                    Coin(self.game, x, y)
                    break  # Thoát vòng lặp sau khi đã tạo đồng xu