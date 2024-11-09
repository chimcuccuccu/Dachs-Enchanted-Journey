import pygame
import pytmx
from pygame.transform import scale

from demo_pygame.src.entities.Enemy import Enemy
from demo_pygame.src.objects.Tree import Objects
from demo_pygame.src.utilz.Config import *

class TiledMap(pygame.sprite.Sprite):
    def __init__(self, filename, game, scale_factor=4):
        super().__init__()
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.scale_factor = scale_factor
        self.width = self.tmxdata.width * self.tmxdata.tilewidth * self.scale_factor
        self.height = self.tmxdata.height * self.tmxdata.tileheight * self.scale_factor
        self.make_map(game)
        self.door_position = None
        self.rect = pygame.Rect(0, 0, self.width, self.height)
    def render_layer(self, surface, layer):
        ti = self.tmxdata.get_tile_image_by_gid
        if isinstance(layer, pytmx.TiledTileLayer):
            # print(f"Rendering TiledTileLayer: {layer.name}")
            for x, y, gid in layer:
                tile = ti(gid)
                if tile:
                    tile = pygame.transform.scale(tile, (tile.get_width() * self.scale_factor, tile.get_height() * self.scale_factor))
                    surface.blit(tile, (x * self.tmxdata.tilewidth * self.scale_factor, y * self.tmxdata.tileheight * self.scale_factor))
                elif isinstance(layer, pytmx.TiledObjectGroup):
                    for obj in layer:
                        if hasattr(obj, 'gid'):
                            tile = ti(obj.gid)
                            if tile:
                                tile = pygame.transform.scale(tile, (
                                tile.get_width() * self.scale_factor, tile.get_height() * self.scale_factor))
                                surface.blit(tile, (obj.x * self.scale_factor, obj.y * self.scale_factor))
                        else:
                            # Load and draw a custom image at the object's coordinates
                            image_path = 'path/to/your/image.png'  # Replace with your image path
                            image = pygame.image.load(image_path).convert_alpha()
                            image = pygame.transform.scale(image, (
                            image.get_width() * self.scale_factor, image.get_height() * self.scale_factor))
                            surface.blit(image, (obj.x * self.scale_factor, obj.y * self.scale_factor))

    def make_map(self, game):
        for layer_index, layer in enumerate(self.tmxdata.visible_layers):
            if isinstance(layer, pytmx.TiledTileLayer):
                layer_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                self.render_layer(layer_surface, layer)
                layer_sprite = pygame.sprite.Sprite()
                layer_sprite.image = layer_surface
                layer_sprite.rect = layer_surface.get_rect()
                print(layer_index, layer)
                if layer_index == 0:
                    layer_sprite._layer = GRASS_LAYER
                elif layer_index == 1:
                    layer_sprite._layer = STREET_LAYER
                elif layer_index == 2:
                    layer_sprite._layer = FLOOR_LAYER
                elif layer_index == 3:
                    layer_sprite._layer = WALL_HOUSE_LAYER
                elif layer_index == 4:
                    layer_sprite._layer = TOP_WALL_HOUSE_LAYER
                elif layer_index == 5:
                    layer_sprite._layer = DECOR_LAYER
                elif layer_index == 6:
                    layer_sprite._layer = CARPET_LAYER

                game.visible_sprites.add(layer_sprite)
                game.all_sprites.add(layer_sprite)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in self.tmxdata.objects:
                    if obj.name == 'Tree-Big':
                        object = Objects(game, obj.x * self.scale_factor, obj.y * self.scale_factor, 60, 90, "../../res/Ngan/Objects_Tiled/Tree-Big.png")
                        game.visible_sprites.add(object)
                        game.all_sprites.add(object)
                        game.collidables.append(object)

                    elif obj.name == 'Tree-Mini':
                        object = Objects(game, obj.x * self.scale_factor, obj.y * self.scale_factor, 30, 30,
                                    "../../res/Ngan/Objects_Tiled/Tree-Mini.png")
                        game.visible_sprites.add(object)
                        game.all_sprites.add(object)
                        game.collidables.append(object)

                    elif obj.name == 'Tree-Tall':
                        object = Objects(game, obj.x * self.scale_factor, obj.y * self.scale_factor, 35, 60,"../../res/Ngan/Objects_Tiled/Tree-Tall.png")
                        game.visible_sprites.add(object)
                        game.all_sprites.add(object)
                        game.collidables.append(object)

                    elif obj.name == 'Wall':
                        object = Objects(game, obj.x * self.scale_factor, obj.y * self.scale_factor, obj.width * 1.5, obj.height * 1.5, image_path=None, load_image=False)
                        # game.visible_sprites.add(object)
                        game.all_sprites.add(object)
                        game.collidables.append(object)

                    elif obj.name == 'Decor':
                        object = Objects(game, obj.x * self.scale_factor, obj.y * self.scale_factor, obj.width * 1.5,
                                         obj.height * 1.5, image_path=None, load_image=False)
                        # game.visible_sprites.add(object)
                        game.all_sprites.add(object)
                        game.collidables.append(object)

                    elif obj.name == 'Rock':
                        object = Objects(game, obj.x * self.scale_factor, obj.y * self.scale_factor, obj.width * 1.5,
                                         obj.height * 1.5, image_path=None, load_image=False)
                        # game.visible_sprites.add(object)
                        game.all_sprites.add(object)
                        game.collidables.append(object)

                    elif obj.name == 'Enemy':
                        enemy = Enemy(game, obj.x * self.scale_factor, obj.y * self.scale_factor)
                        game.visible_sprites.add(enemy)
                        game.all_sprites.add(enemy)
        return pygame.Surface((self.width, self.height), pygame.SRCALPHA)
