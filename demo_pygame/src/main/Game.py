import time

import pygame.display
import pytmx
import subprocess

from demo_pygame.src.entities.EnemySpawner import EnemySpawner
from demo_pygame.src.entities.CoinSpawner import CoinSpawner
from demo_pygame.src.entities.NPC import NPC
from demo_pygame.src.entities.Player import Player
from demo_pygame.src.entities.SpriteSheet import Spritesheet
from demo_pygame.src.levels.Map import TiledMap
from demo_pygame.src.status.Attack import Attack
from demo_pygame.src.status.AttackFire import AttackFire
from demo_pygame.src.status.Dialog import Dialog
from demo_pygame.src.objects.Box import Box
from demo_pygame.src.ui.IconCooldown import IconCooldown
from demo_pygame.src.ui.Scoreboard import Scoreboard
from demo_pygame.src.status.Heal import Heal
from demo_pygame.src.objects.Door import *
from demo_pygame.src.utilz.Config import *
from demo_pygame.src.levels.Level import *


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
        self.coin_spritesheet = Spritesheet('../../res/img/coin.png')
        self.intro_backgroud = pygame.image.load('../../res/img/introbackground.png')
        self.box_spritesheet = Spritesheet('../../res/Ngan/tài nguyên Py/mystic_woods_free_2.2/sprites/objects/chest_01.png')
        self.map_width = 3200
        self.map_height = 1920
        self.score = 0

        self.map_image = pygame.image.load('../../res/img/Map1.png')  # Load your map image
        self.enemy_spawner = EnemySpawner(self, self.map_image)


        self.collidables = []

        self.visible_sprites = YSortCameraGroup()

        self.tmx_data = pytmx.load_pygame('../../res/Ngan/maps/Map1.tmx')

        self.attack_icon = pygame.image.load("../../res/img/attack_icon_64x64.png")
        self.attackfire_icon = pygame.image.load("../../res/img/attackfire_icon_64x64.png")
        self.heal_icon = pygame.image.load("../../res/img/heal_icon_64x64.png")
        self.icon_cooldown = IconCooldown(self)
        self.scoreboard = Scoreboard(self)
        self.challenge_active = False
        self.challenge_start_time = 0
        self.challenge_duration = 30
        self.enemies_destroyed = 0

    def start_enemy_challenge(self):
        self.challenge_active = True
        self.challenge_start_time = time.time()
        self.enemies_destroyed = 0
        self.spawn_enemies_faster()

    def spawn_enemies_faster(self):
        spawner = EnemySpawner(self, self.nganMapSprite)
        spawner.spawn_random_enemies(10)

    def createTilemap(self):
        self.level = TiledMap('../../res/Ngan/maps/Map1.tmx', self)


        level = Level(self, 0, 0)
        self.all_sprites.add(level)

        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h

        self.player = Player(self, 2800, 300)


        self.visible_sprites.add(self.player)
        self.all_sprites.add(self.player)

        self.scoreboard = Scoreboard(self)


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

        spawner_coin = CoinSpawner(self, self.nganMapSprite)
        spawner_coin.spawn_random_coins(20)
        for coin in self.coins:
            self.visible_sprites.add(coin)
            self.all_sprites.add(coin)

        i = 0
        for pos in self.level.box_positions:
            i += 1
            self.box = Box(self, pos[0], pos[1], i)
            self.visible_sprites.add(self.box)
            self.all_sprites.add(self.box)
            self.boxs.add(self.box)
            # self.collidables.append(self.box)

        # for pos in self.level.box_positions:
        #     print (pos[0], pos[1])

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.coins = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.attacksFire = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.heal = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.boxs = pygame.sprite.LayeredUpdates()
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
                    attack.use_skill()  # Cập nhật last_used khi sử dụng
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
                    attack_fire.use_skill()  # Cập nhật last_used khi sử dụng
                elif event.key == pygame.K_c:
                    heal = Heal(self, self.player.rect.x, self.player.rect.y)
                    self.visible_sprites.add(heal) # è è
                    self.all_sprites.add(heal)
                    self.heal.add(heal)
                    heal.use_skill()  # Cập nhật last_used khi sử dụng
                    heal.apply_heal()
                elif event.type == pygame.USEREVENT + 1:
                    # Khôi phục alpha của Player
                    self.player.image.set_alpha(255)  # Trở lại bình thường
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Dừng bộ đếm

    # def start_snake_game(self):
    #     subprocess.run(['python', 'demo_pygame/src/games/snake.py'])

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.visible_sprites.custom_draw(self.player)
        self.clock.tick(FPS)

        self.player.draw_health_bar()
        for npc in self.npcs:
            npc.draw()
        self.icon_cooldown.draw()
        self.scoreboard.draw()
        pygame.display.flip()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass
