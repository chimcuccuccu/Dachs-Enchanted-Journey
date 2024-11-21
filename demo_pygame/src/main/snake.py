import pygame.display
import time
import random


def run_snake_game():
    pygame.init()
    # Initialize pygame
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
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
    snake_speed = 20

    # Fonts
    font_style = pygame.font.SysFont(None, 50)
    score_font = pygame.font.SysFont(None, 35)

    # Functions to display score and message
    def display_score(score):
        value = score_font.render("Score: " + str(score), True, white)
        screen.blit(value, [0, 0])

    def draw_time_bar(start_time, total_time):
        elapsed_time = time.time() - start_time
        remaining_time = total_time - elapsed_time
        if remaining_time < 0:
            remaining_time = 0
        bar_length = (remaining_time / total_time) * screen_width
        pygame.draw.rect(screen, grey, [0, screen_height - 20, screen_width, 20])
        pygame.draw.rect(screen, red, [0, screen_height - 20, bar_length, 20])

    def snake_game():
        print("Starting snake game")

        x1 = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
        y1 = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        def generate_food():
            return (round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block,
                    round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block)

        foodx, foody = generate_food()

        clock = pygame.time.Clock()

        total_time = 30  # Total time for the game in seconds
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change == 0:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change == 0:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change == 0:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change == 0:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
                return False
            x1 += x1_change
            y1 += y1_change
            screen.fill(black)
            pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    return False

            for segment in snake_list:
                pygame.draw.rect(screen, green, [segment[0], segment[1], snake_block, snake_block])

            display_score(length_of_snake - 1)
            draw_time_bar(start_time, total_time)
            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx, foody = generate_food()
                length_of_snake += 1

            # Check if 30 seconds have passed and score is less than 5
            if time.time() - start_time > 30:
                if length_of_snake > 5:
                    return True
                else:
                    return False

            clock.tick(snake_speed)

    return snake_game()
