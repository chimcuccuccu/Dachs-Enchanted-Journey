import pygame

class Collide:
    def __init__(self, game, entity):
        """
        Khởi tạo Collide:
        :param game: Tham chiếu đến lớp Game.
        :param entity: Thực thể (Player hoặc Enemy) cần xử lý va chạm.
        """
        self.game = game
        self.entity = entity  # Ví dụ: Player hoặc Enemy
        self.fade_alpha = 255  # Độ mờ ban đầu của Player (255 là không mờ)

    def collide_enemy(self):
        """ Xử lý va chạm với kẻ địch """
        hits = pygame.sprite.spritecollide(self.entity, self.game.enemies, False)  # Kiểm tra va chạm với kẻ địch
        if hits:
            self.entity.current_health -= 10  # Giảm 10 máu mỗi khi va chạm với Enemy

            # Đảm bảo máu không nhỏ hơn 0
            if self.entity.current_health < 0:
                self.entity.current_health = 0

            # Lấy đối tượng Enemy gần nhất
            enemy_hit = hits[0]

            # Đẩy Player ra khỏi Enemy một khoảng nhỏ (5 pixels)
            push_back_distance = 30  # Khoảng đẩy lùi
            if self.entity.facing == 'left':
                self.entity.rect.x += push_back_distance
            elif self.entity.facing == 'right':
                self.entity.rect.x -= push_back_distance
            elif self.entity.facing == 'up':
                self.entity.rect.y += push_back_distance
            elif self.entity.facing == 'down':
                self.entity.rect.y -= push_back_distance

            # Gọi hiệu ứng mờ
            self.apply_fade_effect()

            # Kiểm tra nếu máu của Player <= 0
            if self.entity.current_health <= 0:
                self.entity.kill()  # Xóa Player khỏi màn hình
                self.game.playing = False  # Dừng trò chơi

    def apply_fade_effect(self):
        """Hiệu ứng mờ cho Player khi va chạm với Enemy."""
        self.fade_alpha = 150  # Giảm độ alpha để tạo hiệu ứng mờ
        self.entity.image.set_alpha(self.fade_alpha)  # Áp dụng alpha mới cho Player

        # Đặt một bộ đếm thời gian để phục hồi alpha về ban đầu sau một khoảng thời gian
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # 500ms hồi phục alpha



