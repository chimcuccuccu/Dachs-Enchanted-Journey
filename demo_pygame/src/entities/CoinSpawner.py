import pygame
import random
import pytmx
from demo_pygame.src.entities.Coin import Coin
from demo_pygame.src.status.MapUtils import MapUtils
from demo_pygame.src.utilz.Config import *

class CoinSpawner:
    def __init__(self, game, map_image):
        self.game = game
        self.map_image = map_image
        self.last_spawn_time = pygame.time.get_ticks()
        self.tmx_data = pytmx.load_pygame('../../res/Ngan/maps/Map1.tmx')
        self.house_positions = MapUtils.get_house_positions(self.tmx_data)
        # print(f"House positions: {self.house_positions}")

    def spawn_random_coins(self, number_of_coins=20):
        tile_size = TILESIZE
        map_width, map_height = self.map_image.get_size()
        chosen_positions = []

        for _ in range(number_of_coins):
            while True:
                x = random.randint(0, map_width // tile_size - 1)
                y = random.randint(0, map_height // tile_size - 1)

                if (x, y) not in chosen_positions and not MapUtils.is_in_house(x, y, tile_size, self.house_positions):
                    chosen_positions.append((x, y))
                    Coin(self.game, x, y)
                    break