import pygame
import subprocess

from demo_pygame.src.status.Dialog import Dialog
from demo_pygame.src.utilz.Config import BOX_LAYER, TILESIZE, BLACK


class Box(pygame.sprite.Sprite):
    def __init__(self, game, x, y, box_id, scale_factor=4):
        self.game = game
        self._layer = BOX_LAYER
        self.groups = self.game.all_sprites, self.game.boxs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 16
        self.height = 16
        self.scale_factor = scale_factor

        self.image = self.game.box_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * self.scale_factor, self.height * self.scale_factor))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.box_id = box_id

        self.is_open = False

    def open(self):
        self.image = self.game.box_spritesheet.get_sprite(16, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * self.scale_factor, self.height * self.scale_factor))
        self.image.set_colorkey(BLACK)
        self.is_open = True

    def close(self):
        self.image = self.game.box_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.width * self.scale_factor, self.height * self.scale_factor))
        self.image.set_colorkey(BLACK)
        self.is_open = False

    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            if not self.is_open:
                self.open()
                print("haha")
                dialog = Dialog(self.game.screen, "Do you want to open the box?", "Yes", "No")
                choice = dialog.show()
                if choice == "Yes":
                    self.handle_yes_option()
                else:
                    self.handle_no_option()
        else:
            self.close()

    def handle_yes_option(self):
        if self.box_id == 1:
            subprocess.run(['python', 'snake.py'])
        elif self.box_id == 2:
            subprocess.run(['python', 'egg_catcher.py'])
        elif self.box_id == 3:
            self.game.start_enemy_challenge()
        print(f"Player chose 'Yes'. Box {self.box_id} opened.")

    def handle_no_option(self):
        # Define the action for the 'No' option
        print("Player chose 'No'. Box remains closed.")