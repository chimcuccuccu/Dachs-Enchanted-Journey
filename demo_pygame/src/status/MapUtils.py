#class này dùng để kiểm tra va chạm giữa các object

import pygame

class MapUtils:
    @staticmethod
    def get_house_positions(tmx_data, scale_factor=4):
        house_positions = []
        for obj in tmx_data.objects:
            if obj.name in ['House', 'Tree-Big', 'Tree-Mini', 'Tree-Tall', 'Rock', 'Decor']:
                house_positions.append(
                    pygame.Rect(obj.x * scale_factor, obj.y * scale_factor, obj.width * scale_factor, obj.height * scale_factor)
                )
        return house_positions

    @staticmethod
    def is_in_house(x, y, tile_size, house_positions):
        coin_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        for house_rect in house_positions:
            if coin_rect.colliderect(house_rect):
                return True
        return False