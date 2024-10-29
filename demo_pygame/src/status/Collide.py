import pygame

from demo_pygame.src.utilz.config import PLAYER_SPEED
from demo_pygame.src.entities.IcePatch import *

class Collide:
    def __init__(self, player):
        """
        Khởi tạo lớp xử lý va chạm cho nhân vật (player).

        :param player: Đối tượng nhân vật cần xử lý va chạm.
        """
        self.player = player
        self.is_bleeding = False  # Trạng thái chảy máu của player
        self.bleed_timer = 0  # Thời gian bắt đầu chảy máu
        self.bleed_duration = 3000  # Thời gian chảy máu kéo dài 3 giây (3000 ms)
        self.bleed_damage_taken = 0  # Lượng sát thương đã gây ra bởi hiệu ứng chảy máu
        self.target_health = 0  # Mức máu cần đạt sau khi hiệu ứng chảy máu hoàn tất

        # Biến để theo dõi trạng thái làm chậm trên băng
        self.is_slowed = False
        self.slow_timer = 0  # Thời gian bắt đầu hiệu ứng làm chậm
        self.slow_duration = 2000  # Thời gian làm chậm kéo dài 2 giây (2000 ms)
        self.original_speed = PLAYER_SPEED  # Sử dụng tốc độ mặc định từ config


    def collide_enemy(self):
        """
        Xử lý va chạm giữa nhân vật và kẻ địch.
        """
        # Kiểm tra va chạm giữa nhân vật và kẻ địch
        hits = pygame.sprite.spritecollide(self.player, self.player.game.enemies, False)
        if hits:
            self.player.health -= 10  # Giảm máu đi 10 mỗi khi bị va chạm

            # Đẩy lùi nhân vật dựa trên hướng mà nhân vật đang đối mặt
            if self.player.facing == 'left':
                self.player.x_change = 30
            elif self.player.facing == 'right':
                self.player.x_change = -30
            elif self.player.facing == 'up':
                self.player.y_change = 30
            elif self.player.facing == 'down':
                self.player.y_change = -30

            # Kiểm tra nếu máu của nhân vật đã hết
            if self.player.health <= 0:
                self.player.kill()  # Xóa nhân vật khỏi trò chơi nếu hết máu
                self.player.game.playing = False  # Kết thúc trò chơi nếu nhân vật chết

    def Collide_bleeding(self):
        """
        Kiểm tra va chạm giữa player và các chướng ngại vật (gai hoặc lửa).
        Nếu có va chạm, kích hoạt và áp dụng hiệu ứng chảy máu trong 3 giây, giảm 30% máu (10% mỗi giây).
        """
        # Kiểm tra va chạm giữa player và nhóm obstacles
        hits = pygame.sprite.spritecollide(self.player, self.player.game.obstacles, False)

        # Nếu có va chạm và player chưa bị chảy máu, bắt đầu chảy máu
        if hits and not self.is_bleeding:
            self.is_bleeding = True
            self.bleed_timer = pygame.time.get_ticks()  # Lưu thời gian bắt đầu chảy máu
            self.bleed_damage_taken = 0  # Đặt lại lượng máu đã mất khi bắt đầu va chạm
            self.target_health = max(self.player.health - 30, 0)  # Giảm 30% máu hoặc tới 0

        # Áp dụng hiệu ứng chảy máu nếu player đang trong trạng thái chảy máu
        if self.is_bleeding:
            current_time = pygame.time.get_ticks()
            time_elapsed = current_time - self.bleed_timer  # Thời gian đã trôi qua

            # Nếu thời gian chảy máu vượt quá 3 giây, dừng chảy máu
            if time_elapsed >= self.bleed_duration:
                self.is_bleeding = False  # Kết thúc hiệu ứng chảy máu
                return

            # Tính toán lượng máu cần trừ theo từng giây
            percentage_per_second = 10  # Mỗi giây mất 10% máu
            seconds_elapsed = time_elapsed // 1000  # Số giây đã trôi qua (0, 1, 2, ...)

            # Tính tổng sát thương cần gây ra tính đến thời điểm này
            total_damage = percentage_per_second * seconds_elapsed

            # Trừ máu dần dần nhưng không vượt quá target_health
            if self.player.health > self.target_health:
                damage_to_take = total_damage - self.bleed_damage_taken
                self.player.health = max(self.player.health - damage_to_take,
                                         self.target_health)  # Trừ máu tới target_health
                self.bleed_damage_taken = total_damage  # Cập nhật lượng sát thương đã gây ra

            # Kiểm tra nếu nhân vật hết máu
            if self.player.health <= 0:
                self.player.kill()  # Nhân vật chết
                self.player.game.playing = False  # Kết thúc trò chơi nếu nhân vật chết

    import pygame
    from demo_pygame.src.utilz.config import PLAYER_SPEED  # Import PLAYER_SPEED từ file config


    def Collide_ice(self):
            """
            Kiểm tra va chạm giữa player và vũng băng (ice) trong all_sprites.
            Nếu có va chạm, giảm 70% tốc độ của player trong 2 giây.
            """
            # Lọc các đối tượng vũng băng trong all_sprites
            ice_patches = [sprite for sprite in self.player.game.all_sprites if getattr(sprite, 'type', None) == 'ice']

            # Kiểm tra va chạm giữa player và vũng băng
            hits = pygame.sprite.spritecollide(self.player, ice_patches, False)

            # Nếu có va chạm và player chưa bị làm chậm, bắt đầu hiệu ứng làm chậm
            if hits and not self.is_slowed:
                self.is_slowed = True
                self.slow_timer = pygame.time.get_ticks()  # Lưu thời gian bắt đầu làm chậm
                self.player.speed = PLAYER_SPEED * 0.3  # Giảm tốc độ xuống còn 30% (làm chậm 70%)

            # Kiểm tra nếu đang trong trạng thái làm chậm
            if self.is_slowed:
                current_time = pygame.time.get_ticks()
                # Nếu thời gian làm chậm vượt quá 2 giây, kết thúc hiệu ứng làm chậm
                if current_time - self.slow_timer >= self.slow_duration:
                    self.is_slowed = False
                    self.player.speed = PLAYER_SPEED  # Khôi phục tốc độ mặc định của player
