import pygame

from demo_pygame.src.utilz.Config import WHITE


class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.score = 0  # Điểm số hiện tại
        self.high_score = 0  # Điểm số cao nhất
        self.font = pygame.font.Font('../../res/fonts/ElecstromRegular-vmyoy.otf', 64)  # Font lớn cho điểm số
        # self.font_small = pygame.font.Font(None, 36)  # Font nhỏ cho điểm số cao nhất
        self.score_text_color = WHITE  # Màu vàng cho điểm số
        self.high_score_text_color = (255, 215, 0)  # Màu vàng đậm cho điểm số cao nhất
        self.background_color = (0, 0, 0, 180)  # Màu nền trong suốt

    def update_score(self, value):
        self.score += value
        if self.score > self.high_score:  # Cập nhật điểm cao nhất
            self.high_score = self.score

    def reset_score(self):
        self.score = 0

    def draw(self):
        # Vẽ điểm số hiện tại
        score_text = self.font.render(f' {self.score}', True, self.score_text_color)
        screen_center_x = self.game.screen.get_rect().centerx
        score_rect = score_text.get_rect(midtop=(screen_center_x, 50))  # Giữa trên cùng
        self.game.screen.blit(score_text, score_rect)

    def add_score(self, value):

        self.update_score(value)
