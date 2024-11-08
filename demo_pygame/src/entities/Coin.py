import math

import pygame
from demo_pygame.src.utilz.Config import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = COIN_LAYER  # Xác định lớp của đồng xu
        self.groups = self.game.all_sprites, self.game.coins  # Thêm đồng xu vào các nhóm cần thiết
        pygame.sprite.Sprite.__init__(self, self.groups)  # Sử dụng super để thêm vào các nhóm

        self.x = x * TILESIZE  # Tọa độ x thực tế của đồng xu
        self.y = y * TILESIZE  # Tọa độ y thực tế của đồng xu
        self.width = TILESIZE  # Chiều rộng đồng xu
        self.height = TILESIZE  # Chiều cao đồng xu

        # Lấy hình ảnh đồng xu từ sprite sheet và thiết lập màu trong suốt
        self.image = self.game.coin_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)

        # Thiết lập hình chữ nhật va chạm
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Thuộc tính bổ sung cho đồng xu
        self.value = 10  # Giá trị của đồng xu
        self.lifetime = 30000  # Thời gian tồn tại của đồng xu tính bằng milliseconds
        self.spawn_time = pygame.time.get_ticks()  # Thời gian mà đồng xu được tạo ra

        # Tạo âm thanh thu thập xu
        self.coin_sound = pygame.mixer.Sound('../../res/Ngan/sound_effects/coin_sound.wav')

        # Hiệu ứng nảy lên xuống
        self.nudge_speed = 0.01  # Giảm tốc độ nảy lên xuống (làm cho đồng xu nảy chậm hơn)
        self.amplitude = 4  # Biên độ (chiều cao) của chuyển động nảy
        self.offset = 0  # Dịch chuyển mặc định của đồng xu khi sinh ra

        # Khởi tạo scale_factor cho việc thu nhỏ đồng xu
        self.scale_factor = 1  # Tỉ lệ ban đầu là 1 (đồng xu có kích thước bình thường)
        self.scale_rate = 0.05  # Tỉ lệ thu nhỏ của đồng xu

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

        # Kiểm tra va chạm với người chơi để thu thập xu
        if pygame.sprite.collide_rect(self, self.game.player):
            self.collect_coin()

        self.offset = math.sin(pygame.time.get_ticks() * self.nudge_speed) * self.amplitude
        self.rect.y = self.y + self.offset

        # Nếu đồng xu đang được thu nhỏ, giảm kích thước của nó
        if self.scale_factor < 0.1:  # Khi đồng xu đã quá nhỏ
            self.kill()
        elif self.scale_factor < 1:  # Thu nhỏ đồng xu dần dần
            self.scale_factor -= self.scale_rate
            self.image = pygame.transform.scale(self.game.coin_spritesheet.get_sprite(0, 0, self.width, self.height),
                                                (int(self.width * self.scale_factor),
                                                 int(self.height * self.scale_factor)))
            self.rect = self.image.get_rect(center=self.rect.center)

    def collect_coin(self):
        self.coin_sound.play()
        self.game.scoreboard.update_score(self.value)
        self.scale_factor = 1
        self.kill()