import time

import pygame
from itertools import cycle
from random import randrange


def egg_play():
    start_time = time.time()
    total_time = 30
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Egg Catcher")

    color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
    egg_width = 45
    egg_height = 55
    egg_score = 10
    egg_speed = 400
    egg_interval = 4000
    difficulty = 0.95
    catcher_color = (0, 0, 255)
    catcher_width = 100
    catcher_height = 100
    catcher_startx = screen_width / 2 - catcher_width / 2
    catcher_starty = screen_height - catcher_height - 20

    catcher = pygame.Rect(catcher_startx, catcher_starty, catcher_width, catcher_height)
    font = pygame.font.SysFont(None, 50)

    score = 0
    lives_remaining = 3
    eggs = []
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    grey = (169, 169, 169)

    def draw_time_bar(start_time, total_time):
        elapsed_time = time.time() - start_time
        remaining_time = total_time - elapsed_time
        if remaining_time < 0:
            remaining_time = 0
        bar_length = (remaining_time / total_time) * screen_width
        pygame.draw.rect(screen, grey, [0, screen_height - 20, screen_width, 20])
        pygame.draw.rect(screen, red, [0, screen_height - 20, bar_length, 20])

    def create_egg():
        x = randrange(10, screen_width - egg_width)
        y = 40
        new_egg = pygame.Rect(x, y, egg_width, egg_height)
        eggs.append(new_egg)

    def move_eggs():
        for egg in eggs:
            egg.move_ip(0, 30)
            if egg.bottom > screen_height:
                eggs.remove(egg)
                lose_a_life()

    def lose_a_life():
        nonlocal lives_remaining
        lives_remaining -= 1

    def check_catch():
        nonlocal score, egg_speed, egg_interval
        for egg in eggs:
            if catcher.colliderect(egg):
                eggs.remove(egg)
                score += egg_score
                egg_speed = int(egg_speed * difficulty)
                egg_interval = int(egg_interval * difficulty)

    def draw():
        screen.fill((0, 191, 255))
        # deep sky blue
        pygame.draw.rect(screen, (46, 139, 87), (0, screen_height - 100, screen_width, 100))  # sea green
        pygame.draw.ellipse(screen, (255, 165, 0), (-80, -80, 200, 200))  # orange
        pygame.draw.arc(screen, catcher_color, catcher, 3.14, 0, 3)  # reversed upward
        for egg in eggs:
            pygame.draw.ellipse(screen, next(color_cycle), egg)
        score_text = font.render(f"Score: {score}", True, (0, 0, 139))
        lives_text = font.render(f"Lives: {lives_remaining}", True, (0, 0, 139))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (screen_width - 150, 10))
        # pygame.display.flip()

    running = True
    clock = pygame.time.Clock()
    egg_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(egg_timer, egg_interval)

    move_left = False
    move_right = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False
            elif event.type == egg_timer:
                create_egg()

        if move_left and catcher.left > 0:
            catcher.move_ip(-20, 0)
        if move_right and catcher.right < screen_width:
            catcher.move_ip(20, 0)

        # Check if 30 seconds have passed and score is more than or equal to 30
        if time.time() - start_time >= 30:
            if score >= 30:
                return True
            else:
                return False

        if lives_remaining <= 0:
            return False
        move_eggs()
        check_catch()
        draw()
        draw_time_bar(start_time, total_time)
        pygame.display.update()
        clock.tick(20)
