import pygame

import math
from demo_pygame.src.utilz.Config import *


class Heal(pygame.sprite.Sprite):
    cooldown = 10000  # Cooldown của Heal là 5 giây
    last_used = 0  # Lần sử dụng gần nhất của Heal
    def __init__(self, game, x, y, scale_factor=1.3):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.heal
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE + 16

        self.scale_factor = scale_factor
        self.animation_loop = 0
        self.animation_speed = 0.25
        self.healed = False  # Đảm bảo chỉ hồi máu một lần

        self.image = self.game.heal_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y - TILESIZE // 2

    @classmethod
    def can_create(cls):
        # """Kiểm tra nếu có thể tạo Attack dựa trên cooldown."""
        # current_time = pygame.time.get_ticks()
        # if current_time - cls.last_used >= cls.cooldown:
        #     cls.last_used = current_time
        #     return True
        # return False
        """Kiểm tra nếu cooldown đã hết mà không cập nhật last_used."""
        current_time = pygame.time.get_ticks()
        return (current_time - cls.last_used) >= cls.cooldown

    def use_skill(self):
        """Gọi khi kỹ năng thực sự được kích hoạt để cập nhật last_used."""
        if self.can_create():
            self.__class__.last_used = pygame.time.get_ticks()
            # Thực hiện các hành động khác khi sử dụng kỹ năng

    def update(self):
        self.animate()

    def animate(self):
        heal_animations = [self.game.heal_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(32, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(64, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(96, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(128, 0, self.width, self.height),
                            self.game.heal_spritesheet.get_sprite(160, 0, self.width, self.height),]

        self.image = heal_animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.25
        if self.animation_loop >= 5:
            self.kill()

    def apply_heal(self):
        """Thực hiện logic hồi máu."""
        if not self.healed:
            heal_amount = self.game.player.max_health * 0.5  # Hồi 50% máu tối đa
            self.game.player.heal(heal_amount)  # Gọi phương thức heal của Player
            self.healed = True  # Đảm bảo hồi máu chỉ 1 lần