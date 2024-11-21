# demo_pygame/src/entities/NPC.py

import pygame

from demo_pygame.src.utilz.Config import NPC_LAYER

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, image_path):
        dialog_texts = [
            "Nhấn Enter!",
            "A lô",
            "Bố em là người khó tính",
            "Nếu anh muốn lấy em làm vợ",
            "Thì anh phải thu thập đủ 5 hòm...",
            "...sính lễ",
            "Bố em mới chịu cơ",
            "Anh đi ra ngoài vườn mà tìm",
            "Cố lên anh nhớ!!!"
        ]
        super().__init__()
        self._layer = NPC_LAYER
        self.game = game
        self.image = pygame.image.load(image_path)
        self.groups = self.game.all_sprites, self.game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        custom_font = pygame.font.Font('../../res/fonts/Ganh Type - Regular.otf', 28)  # Specify the path to your custom font
        self.dialog = Dialog(game.screen, dialog_texts, custom_font, npc_rect=self.rect)
        self.last_dialog_time = 0  # Initialize the last dialog time
        self.expanded_rect = self.rect.inflate(10, 10)

    def update(self):
        if self.expanded_rect.colliderect(self.game.player.rect):
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_RETURN] and current_time - self.last_dialog_time > 300:  # 500 milliseconds = 0.5 seconds
                self.dialog.next_dialog()
                self.last_dialog_time = current_time  # Update the last dialog time

    def draw(self):
        self.dialog.draw()

class Dialog:
    def __init__(self, screen, dialog_texts, font, text_color=(255, 255, 255), bg_color=(0, 0, 0), npc_rect=None, max_width=400):
        self.screen = screen
        self.dialog_texts = dialog_texts
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.current_index = 0
        self.npc_rect = npc_rect  # NPC's position to anchor the dialog
        self.max_width = max_width  # Maximum width for the dialog text

    def draw(self):
        if self.is_finished():
            return
        # Position the dialog above the NPC's head
        dialog_x = 1290
        dialog_y = 100

        # Render dialog text with wrapping
        lines = self.wrap_text(self.dialog_texts[self.current_index])
        y_offset = 0
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(dialog_x, dialog_y + y_offset))
            y_offset += text_rect.height

            # Background box for text
            bg_rect = text_rect.inflate(10, 10)  # Slight padding around the text
            pygame.draw.rect(self.screen, self.bg_color, bg_rect)

            self.screen.blit(text_surface, text_rect)

    def wrap_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if self.font.size(test_line)[0] <= self.max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)
        return lines

    def next_dialog(self):
        if self.current_index < len(self.dialog_texts) - 1 and self.current_index != -1:
            self.current_index += 1
        else:
            self.current_index = -1  # End of dialog

    def is_finished(self):
        return self.current_index == -1

    def reset(self):
        self.current_index = 0