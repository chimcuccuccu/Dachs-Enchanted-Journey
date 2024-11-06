import pygame, sys
from demo_pygame.src.ui.Button import *
import cv2
from demo_pygame.src.main.Game import Game
from demo_pygame.src.utilz.Config import WIN_WIDTH, WIN_HEIGHT

pygame.init()
pygame.font.init()
pygame.mixer.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

video = cv2.VideoCapture('../../res/Buttons/back_ground.mp4')

button_click_sound = pygame.mixer.Sound('../../res/Ngan/sound_effects/button_pressed.mp3')
button_hover_sound = pygame.mixer.Sound('../../res/Ngan/sound_effects/button_pressed.mp3')

def get_font(size):
    return pygame.font.Font('../../res/fonts/ChangaOne-Regular.ttf', size)

def get_font_button(size):
    return pygame.font.Font('../../res/fonts/Bungee-Regular.otf', size)

def fade(screen, width, height, color=(0, 0, 0), speed=5):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill(color)
    for alpha in range(0, 255, speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(1)

def play():
    fade(SCREEN, screen_width, screen_height)
    game = Game()
    game.new()
    game.main()

    while True:
        if not game.running:
            game_over_screen()
            return

def main_menu():
    clock = pygame.time.Clock()

    name_back_image = pygame.image.load('../../res/Buttons/NameBack.png')
    name_back_image = pygame.transform.scale(name_back_image, (800, 200))

    while True:
        ret, frame = video.read()
        if not ret:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen_width, screen_height))
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        frame = pygame.transform.flip(frame, True, False)

        SCREEN.blit(frame, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(135).render("MAIN MENU", True, "#fde294")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width // 2, 200))

        base_image = pygame.image.load("../../res/Buttons/Play_Default.png")
        base_image = pygame.transform.scale(base_image, (280, 120))

        hover_image = pygame.image.load('../../res/Buttons/Play_Hover.png')
        hover_image = pygame.transform.scale(hover_image, (280, 120))

        button_x = screen_width // 2
        button_y = screen_height // 2
        
        PLAY_BUTTON = Button(image=base_image, pos=(button_x, button_y), base_image=base_image, hover_image=hover_image,
                             text_input="PLAY", font=get_font_button(60), base_color="#a4925f", hovering_color="#a4925f", text_offset=(0, 0), click_sound=button_click_sound)

        QUIT_BUTTON = Button(image=base_image, pos=(button_x, button_y + 150), base_image=base_image, hover_image=hover_image,
                             text_input="QUIT", font=get_font_button(60), base_color="#a4925f", hovering_color="#a4925f", text_offset=(0, 0), click_sound=button_click_sound)

        name_back_rect = name_back_image.get_rect(center=MENU_RECT.center)

        SCREEN.blit(name_back_image, name_back_rect)
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_click_sound.play()
                    fade(SCREEN, screen_width, screen_height)
                    play()
                    return
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    fade(SCREEN, screen_width, screen_height)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(200)

def game_over_screen():
    while True:
        SCREEN.fill("black")

        GAME_OVER_TEXT = get_font(150).render("GAME OVER", True, "#740938")
        GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(screen_width // 2, 200))

        PLAY_AGAIN_TEXT = get_font(50).render("PLAY AGAIN?", True, "#740938")
        PLAY_AGAIN_RECT = PLAY_AGAIN_TEXT.get_rect(center=(screen_width // 2, 350))

        SCREEN.blit(GAME_OVER_TEXT, GAME_OVER_RECT)
        SCREEN.blit(PLAY_AGAIN_TEXT, PLAY_AGAIN_RECT)

        button_x = screen_width // 2
        button_y = screen_height // 2

        base_image = pygame.image.load("../../res/Buttons/Play_Default.png")
        base_image = pygame.transform.scale(base_image, (280, 120))

        hover_image = pygame.image.load('../../res/Buttons/Play_Hover.png')
        hover_image = pygame.transform.scale(hover_image, (280, 120))

        RESTART_BUTTON = Button(image=base_image, pos=(button_x + 300, button_y + 100), base_image=base_image, hover_image=hover_image,
                             text_input="YES", font=get_font_button(50), base_color="#a4925f", hovering_color="#a4925f", text_offset=(0, 0))

        QUIT_BUTTON = Button(image=base_image, pos=(button_x - 300, button_y + 100), base_image=base_image, hover_image=hover_image,
                             text_input="NO", font=get_font_button(60), base_color="#a4925f", hovering_color="#a4925f", text_offset=(0, 0))

        MOUSE_POS = pygame.mouse.get_pos()

        RESTART_BUTTON.changeColor(MOUSE_POS)
        QUIT_BUTTON.changeColor(MOUSE_POS)

        RESTART_BUTTON.update(SCREEN)
        QUIT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESTART_BUTTON.checkForInput(MOUSE_POS):
                    fade(SCREEN, screen_width, screen_height)
                    play()
                    return
                if QUIT_BUTTON.checkForInput(MOUSE_POS):
                    fade(SCREEN, screen_width, screen_height)
                    main_menu()
                    return

        pygame.display.update()

main_menu()