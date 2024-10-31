import pygame

class Button():
    def __init__(self, image, pos, base_image, hover_image, text_input=None, font=None, base_color="White", hovering_color="Green", text_offset = (0, 0)):
        self.image = image
        self.base_image = base_image
        self.hover_image = hover_image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_offset = text_offset
        self.text = self.font.render(self.text_input, True, self.base_color) if self.text_input else None
        if self.text:
            self.text_rect = self.text.get_rect(center=(self.x_pos + self.text_offset[0], self.y_pos + self.text_offset[1]))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        if self.text:
            screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.hover_image
            if self.text:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.image = self.base_image
            if self.text:
                self.text = self.font.render(self.text_input, True, self.base_color)