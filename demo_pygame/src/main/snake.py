import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (169, 169, 169)

# Snake settings
snake_block = 20
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Functions to display score and message
def display_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

def draw_time_bar(start_time, total_time):
    elapsed_time = time.time() - start_time
    remaining_time = total_time - elapsed_time
    if remaining_time < 0:
        remaining_time = 0
    bar_length = (remaining_time / total_time) * screen_width
    pygame.draw.rect(screen, grey, [0, screen_height - 20, screen_width, 20])
    pygame.draw.rect(screen, red, [0, screen_height - 20, bar_length, 20])

# Main game function
def snake_game():
    print("Starting snake game")
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0

    clock = pygame.time.Clock()

    total_time = 30  # Total time for the game in seconds
    start_time = time.time()

    while not game_over:
        print("Game loop running")
        while game_close:
            print("Game close loop running")
            screen.fill(black)
            display_message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("Quit key pressed")
                        return False
                    if event.key == pygame.K_c:
                        print("Play again key pressed")
                        return snake_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Pygame quit event")
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for segment in snake_list:
            pygame.draw.rect(screen, green, [segment[0], segment[1], snake_block, snake_block])

        display_score(length_of_snake - 1)
        draw_time_bar(start_time, total_time)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
            length_of_snake += 1

        # Check if 30 seconds have passed and score is less than 10
        if time.time() - start_time > 30 and length_of_snake - 1 < 10:
            game_close = True

        clock.tick(snake_speed)

    pygame.quit()
    print("Exiting snake game")
snake_game()