import pygame
import sys

from demo_pygame.src.utilz.Config import DIALOG_LAYER

class Dialog:
    def __init__(self, screen, message, option1, option2):
        self._layer = DIALOG_LAYER
        self.screen = screen
        self.message = message
        self.option1 = option1
        self.option2 = option2
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.dialog_width, self.dialog_height = 400, 200
        self.dialog_rect = pygame.Rect((screen.get_width() - self.dialog_width) // 2,
                                       (screen.get_height() - self.dialog_height) // 2,
                                       self.dialog_width, self.dialog_height)
        self.option1_rect = pygame.Rect(self.dialog_rect.x + 50, self.dialog_rect.y + 100, 100, 50)
        self.option2_rect = pygame.Rect(self.dialog_rect.x + 250, self.dialog_rect.y + 100, 100, 50)

    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.option1_rect.collidepoint(event.pos):
                        return self.option1
                    elif self.option2_rect.collidepoint(event.pos):
                        return self.option2

            pygame.draw.rect(self.screen, (255, 255, 255), self.dialog_rect)
            pygame.draw.rect(self.screen, (0, 255, 0), self.option1_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.option2_rect)

            message_surface = self.font.render(self.message, True, (0, 0, 0))
            option1_surface = self.font.render(self.option1, True, (0, 0, 0))
            option2_surface = self.font.render(self.option2, True, (0, 0, 0))

            self.screen.blit(message_surface, (self.dialog_rect.x + 20, self.dialog_rect.y + 20))
            self.screen.blit(option1_surface, (self.option1_rect.x + (self.option1_rect.width - option1_surface.get_width()) // 2,
                                               self.option1_rect.y + (self.option1_rect.height - option1_surface.get_height()) // 2))
            self.screen.blit(option2_surface, (self.option2_rect.x + (self.option2_rect.width - option2_surface.get_width()) // 2,
                                               self.option2_rect.y + (self.option2_rect.height - option2_surface.get_height()) // 2))

            pygame.display.flip()
            self.clock.tick(30)