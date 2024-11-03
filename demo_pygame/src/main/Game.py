import pygame
import pytmx

from demo_pygame.src.entities.Enemy import Enemy
from demo_pygame.src.entities.EnemySpawner import EnemySpawner
from demo_pygame.src.entities.Player import Player
from demo_pygame.src.entities.SpriteSheet import Spritesheet
from demo_pygame.src.levels.Map import TiledMap
from demo_pygame.src.status.Attack import Attack
from demo_pygame.src.status.AttackFire import AttackFire
from demo_pygame.src.status.Heal import Heal
from demo_pygame.src.ui.Button import Button
from demo_pygame.src.ui.Door import Door
from demo_pygame.src.utilz.Config import *
from demo_pygame.src.levels.Level import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.font = pygame.font.Font(None, 36)
        screen_width = info.current_w
        screen_height = info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.running = True
        self.nganMapSprite = Spritesheet('../../res/img/Map1.png')
        self.character_spritesheet = Spritesheet('../../res/img/character.png')
        self.terrain_spritesheet = Spritesheet('../../res/img/terrain.png')
        self.enemy_spritesheet = Spritesheet('../../res/img/enemy.png')
        self.attack_spritesheet = Spritesheet('../../res/img/attack.png')
        self.door_spritesheet = Spritesheet('../../res/Ngan/tài nguyên Py/mystic_woods_free_2.2/sprites/tilesets/walls/wooden_door.png')
        self.attackFire_spritesheet = Spritesheet('../../res/img/fireball.png')
        self.heal_spritesheet = Spritesheet('../../res/img/heal.png')
        self.intro_backgroud = pygame.image.load('../../res/img/introbackground.png')
        self.map_width = 3200
        self.map_height = 1920

        self.visible_sprites = YSortCameraGroup()

        self.tmx_data = pytmx.load_pygame('../../res/Ngan/maps/Map1.tmx')
    def createTilemap(self):
        # self.level = Level(self, 0, 0)
        self.level = TiledMap('../../res/Ngan/maps/Map1.tmx', self)
        # self.visible_sprites.add(self.level)
        # self.all_sprites.add(self.level)

        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h

        self.player = Player(self, 2800, 300)


        self.visible_sprites.add(self.player)
        self.all_sprites.add(self.player)

        # self.visible_sprites.add(self.attacks)
        self.all_sprites.add(self.attacks)

        # self.visible_sprites.add(self.attacksFire)
        self.all_sprites.add(self.attacksFire)

        # self.visible_sprites.add(self.heal)
        self.all_sprites.add(self.heal)

        # Khởi tạo EnemySpawner và spawn 3 kẻ thù ngẫu nhiên
        spawner = EnemySpawner(self, self.nganMapSprite)
        spawner.spawn_random_enemies(3)
        for enemy in self.enemies:
            self.visible_sprites.add(enemy)
            self.all_sprites.add(enemy)

        # vì cửa 16x16 nen phai chia ti le cho dung
        door_x = 41 * 2
        door_y = 9 * 2
        self.door = Door(self, door_x, door_y)
        self.visible_sprites.add(self.door)
        self.all_sprites.add(self.door)
        self.doors.add(self.door)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.attacksFire = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.heal = pygame.sprite.LayeredUpdates()
        self.level = pygame.sprite.LayeredUpdates()
        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        attack = Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        attack = Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        attack = Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        attack = Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
                    self.visible_sprites.add(attack) # (*ngan*) cái này để cho mấy cái status hiện lên màn hình á
                    self.all_sprites.add(attack)
                    self.attacks.add(attack)        # cái này nữa, mấy cái bên dưới nữa
                elif event.key == pygame.K_h:
                    direction = self.player.facing
                    if self.player.facing == 'up':
                        attack_fire = AttackFire(self, self.player.rect.x - 8, self.player.rect.y - TILESIZE, direction)
                    if self.player.facing == 'down':
                        attack_fire = AttackFire(self, self.player.rect.x - 8, self.player.rect.y + TILESIZE, direction)
                    if self.player.facing == 'left':
                        attack_fire = AttackFire(self, self.player.rect.x - TILESIZE, self.player.rect.y - 8, direction)
                    if self.player.facing == 'right':
                        attack_fire = AttackFire(self, self.player.rect.x + TILESIZE, self.player.rect.y - 8, direction)
                    self.visible_sprites.add(attack_fire) # nè nè
                    self.all_sprites.add(attack_fire)
                    self.attacksFire.add(attack_fire) # đay nữa
                elif event.key == pygame.K_c:
                    heal = Heal(self, self.player.rect.x, self.player.rect.y)
                    self.visible_sprites.add(heal) # è è
                    self.all_sprites.add(heal)
                    self.heal.add(heal)


    def update(self):
        self.all_sprites.update()

        door_hits = pygame.sprite.spritecollide(self.player, self.doors, False)
        for door in door_hits:
            door.open()

    def draw(self):
        self.screen.fill(BLACK)
        self.visible_sprites.custom_draw(self.player)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

