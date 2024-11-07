import pygame

class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.score = 0  # Điểm số hiện tại
        self.high_score = 0  # Điểm số cao nhất
        self.font = pygame.font.Font(None, 64)  # Font lớn cho điểm số
        self.font_small = pygame.font.Font(None, 36)  # Font nhỏ cho điểm số cao nhất
        self.score_text_color = (255, 255, 0)  # Màu vàng cho điểm số
        self.high_score_text_color = (255, 215, 0)  # Màu vàng đậm cho điểm số cao nhất
        self.background_color = (0, 0, 0, 180)  # Màu nền trong suốt

    def update_score(self, value):
        self.score += value
        if self.score > self.high_score:  # Cập nhật điểm cao nhất
            self.high_score = self.score

    def reset_score(self):
        self.score = 0

    def draw(self):
        # Vẽ nền bảng điểm
        pygame.draw.rect(self.game.screen, self.background_color, (10, 10, 300, 120), border_radius=10)  # Rectangle với góc bo tròn

        # Vẽ điểm số hiện tại
        score_text = self.font.render(f'Score: {self.score}', True, self.score_text_color)
        score_rect = score_text.get_rect(center=(160, 50))  # Giữa
        self.game.screen.blit(score_text, score_rect)

        # Vẽ điểm số cao nhất
        high_score_text = self.font_small.render(f'High Score: {self.high_score}', True, self.high_score_text_color)
        high_score_rect = high_score_text.get_rect(center=(160, 90))  # Giữa
        self.game.screen.blit(high_score_text, high_score_rect)

    def add_score(self, value):

        self.update_score(value)
