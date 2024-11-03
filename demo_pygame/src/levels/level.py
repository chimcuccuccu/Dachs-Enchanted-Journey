import pygame

from demo_pygame.src.utilz.Config import GROUND_LAYER, TILESIZE, PLAYER_LAYER
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
        self.image = pygame.image.load('../../res/img/Map1.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        for door in self.game.doors:
            door.update()

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
        self.floor_surf_original = pygame.image.load('../../res/img/Map1.png').convert()
        self.floor_rect = self.floor_surf_original.get_rect(topleft=(0,0))

    def custom_draw(self,player):

       # Khởi tạo phần bù
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Đảm bảo phần bù không ra khỏi ranh giới của map
        self.offset.x = max(0, min(self.offset.x, self.floor_rect.width - self.display_surface.get_width()))
        self.offset.y = max(0, min(self.offset.y, self.floor_rect.height - self.display_surface.get_height()))

        # player_layer = PLAYER_LAYER
        # for sprite in self.sprites():
        #     if sprite != player:
        #         if player.rect.centery > sprite.rect.centery:
        #             player_layer = max(player_layer, sprite._layer + 1)
        #         else:
        #             player_layer = min(player_layer, sprite._layer - 1)
        # player._layer = player_layer

        #New code
        # for sprite in sorted(self.sprites(), key=lambda sprite: (sprite._layer, sprite.rect.centery)):
        #     offset_pos = sprite.rect.topleft - self.offset
        #     self.display_surface.blit(sprite.image, offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite._layer):
                   offset_pos = sprite.rect.topleft - self.offset
                   self.display_surface.blit(sprite.image, offset_pos)