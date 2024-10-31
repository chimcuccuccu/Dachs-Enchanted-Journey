import pygame

from demo_pygame.src.entities.Enemy import Enemy
from demo_pygame.src.entities.EnemySpawner import EnemySpawner
from demo_pygame.src.entities.Player import Player
from demo_pygame.src.entities.SpriteSheet import Spritesheet
from demo_pygame.src.status.Attack import Attack
from demo_pygame.src.status.AttackFire import AttackFire
from demo_pygame.src.status.Heal import Heal
from demo_pygame.src.ui.Button import Button
from demo_pygame.src.utilz.config import *
from demo_pygame.src.levels.level import *
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
        self.nganMapSprite = Spritesheet('../../res/Ngan/maps/Ground.png')
        self.character_spritesheet = Spritesheet('../../res/img/character.png')
        self.terrain_spritesheet = Spritesheet('../../res/img/terrain.png')
        self.enemy_spritesheet = Spritesheet('../../res/img/enemy.png')
        self.attack_spritesheet = Spritesheet('../../res/img/attack.png')
        self.attackFire_spritesheet = Spritesheet('../../res/img/fireball.png')
        self.heal_spritesheet = Spritesheet('../../res/img/heal.png')
        self.intro_backgroud = pygame.image.load('../../res/img/introbackground.png')
        self.map_width = 3200
        self.map_height = 1920

        self.visible_sprites = YSortCameraGroup()

    def createTilemap(self):
        self.level = Level(self, 0, 0)
        self.visible_sprites.add(self.level)
        self.all_sprites.add(self.level)

        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h

        self.player = Player(self, screen_width / 2, screen_height / 2)

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

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.attacksFire = pygame.sprite.LayeredUpdates()
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

    # def intro_screen(self):
    #     intro = True
    #
    #     title = self.font.render('Awesome Game', True, BLACK)
    #     title_rect = title.get_rect(x = 10, y = 10)
    #
    #     play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)
    #
    #     while intro:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 intro = False
    #                 self.running = False
    #
    #         mouse_pos = pygame.mouse.get_pos()
    #         mouse_pressed = pygame.mouse.get_pressed()
    #
    #         if play_button.is_pressed(mouse_pos, mouse_pressed):
    #             intro = False
    #
    #         self.screen.blit(self.intro_backgroud, (0, 0))
    #         self.screen.blit(title, title_rect)
    #         self.screen.blit(play_button.image, play_button.rect)
    #         self.clock.tick(FPS)
    #         pygame.display.update()

