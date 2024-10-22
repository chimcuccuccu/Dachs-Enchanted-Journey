from venv import create

import pygame
from pygame.examples.music_drop_fade import SCREEN_SIZE
from pygame.examples.scrap_clipboard import screen

from config import *
from demo_pygame.level import Level
from sprites import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()

        screen_width = info.current_w
        screen_height = info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Arialn.ttf', 32)
        self.running = True
        self.nganMapSprite = Spritesheet('img/Map1.png')
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.attackFire_spritesheet = Spritesheet('img/fireball.png')
        self.heal_spritesheet = Spritesheet('img/heal.png')
        self.intro_backgroud = pygame.image.load('img/introbackground.png')

    def createTilemap(self):
        level = Level(self, 0, 0)
        self.all_sprites.add(level)
        self.player = Player(self, 100, 100)
        for i, row in enumerate(tilemap):
            for j, col in enumerate(row):
                # if col == "B":
                #     Block(self, j, i)
                if col == "E":
                    Enemy(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.attacksFire = pygame.sprite.LayeredUpdates()
        self.heal = pygame.sprite.LayeredUpdates()
        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
                elif event.key == pygame.K_h:
                    direction = self.player.facing
                    if self.player.facing == 'up':
                        AttackFire(self, self.player.rect.x - 8, self.player.rect.y - TILESIZE, direction)
                    if self.player.facing == 'down':
                        AttackFire(self, self.player.rect.x - 8, self.player.rect.y + TILESIZE, direction)
                    if self.player.facing == 'left':
                        AttackFire(self, self.player.rect.x - TILESIZE, self.player.rect.y - 8, direction)
                    if self.player.facing == 'right':
                        AttackFire(self, self.player.rect.x + TILESIZE, self.player.rect.y - 8, direction)
                elif event.key == pygame.K_c:
                    Heal(self, self.player.rect.x, self.player.rect.y)


    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
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

    def intro_screen(self):
        intro = True

        title = self.font.render('Awesome Game', True, BLACK)
        title_rect = title.get_rect(x = 10, y = 10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_backgroud, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()



