from distutils.core import setup

import pygame

from demo_pygame.src.utilz.Generic import Generic
from demo_pygame.src.utilz.config import GROUND_LAYER, TILESIZE, HOUSE_FLOOR
from pytmx.util_pygame import load_pygame


class Level(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.level


        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = pygame.image.load('../../res/Ngan/maps/Ground.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.all_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

    def setup(self):
        tmx_data = load_pygame('../../res/Ngan/maps/Map1.tmx')

        for x, y, surf in tmx_data.get_layer_by_name('floor').tiles():
            Generic((x * TILESIZE, y * TILESIZE), surf, self.all_sprites, HOUSE_FLOOR)

        Generic (
            pos = (0, 0),
            surf = pygame.image.load('../../res/Ngan/maps/Ground.png').convert_alpha(),
            groups= self.all_sprites,
            z = GROUND_LAYER
        )
    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

#Hàm này để tạo camera cho nhân vật
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()


        #creating the floor
        self.floor_surf_original = pygame.image.load('../../res/Ngan/maps/Ground.png').convert()
        self.floor_rect = self.floor_surf_original.get_rect(topleft=(0,0))

    def custom_draw(self,player):

       # Khởi tạo phần bù
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Đảm bảo phần bù không ra khỏi ranh giới của map
        self.offset.x = max(0, min(self.offset.x, self.floor_rect.width - self.display_surface.get_width()))
        self.offset.y = max(0, min(self.offset.y, self.floor_rect.height - self.display_surface.get_height()))

        #drawing the floor
        # floor_offset_pos = self.floor_rect.topleft - self.offset
        # self.display_surface.blit(self.floor_surf_original, floor_offset_pos)


        #New code
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite._layer):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # Old code, not draw in the sprite layer order
        # for sprite in self.sprites():
        # for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
        #     offset_pos = sprite.rect.topleft - self.offset
        #     self.display_surface.blit(sprite.image,offset_pos)
