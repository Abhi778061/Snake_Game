import pygame
import time
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 180, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Snake and food size
block_size = 20
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
large_font = pygame.font.SysFont("bahnschrift", 40)

# Sound and music
try:
    pygame.mixer.music.load("background_music.mp3")
    eat_sound = pygame.mixer.Sound("eat.wav")
    game_over_sound = pygame.mixer.Sound("gameover.wav")
except:
    print("⚠️ Sound files not found. Sounds will be disabled.")
    pygame.mixer.music.load = lambda x: None
    eat_sound = game_over_sound = pygame.mixer.Sound = lambda x: None

# Score display
def score_display(score, high_score, level):
    value = font_style.render(f"Score: {score}  High Score: {high_score}  Level: {level}", True, white)
    win.blit(value, [10, 10])

# Draw snake blocks
def draw_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], block, block])

# Message display
def message(msg, color, y_offset=0):
    mesg = large_font.render(msg, True, color)
    win.blit(mesg, [width / 6, height / 3 + y_offset])

# High score file management
def load_high_score():
    if not os.path.exists("highscore.txt"):
        return 0
    with open("highscore.txt", "r") as f:
        return int(f.read())

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Main menu loop
def main_menu():
    win.fill(black)
    message("SNAKE GAME", yellow, -50)
    message("Press SPACE to Start", white, 10)
    message("Press Q to Quit", red, 60)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False

# Main game loop
def game_loop():
    if not main_menu():
        return

    try:
        pygame.mixer.music.play(-1)
    except:
        pass

    game_over = False
    game_close = False

    x = width / 2
    y = height / 2
    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0

    level = 1
    speed = 10
    high_score = load_high_score()

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()
            try:
                game_over_sound.play()
            except:
                pass
            win.fill(black)
            message("Game Over!", red, -30)
            message("Press C to Play Again or Q to Quit", white, 30)
            score_display(length_of_snake - 1, high_score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = block_size
                    x_change = 0

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        win.fill(black)

        pygame.draw.rect(win, blue, [food_x, food_y, block_size, block_size])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(block_size, snake_list)
        score_display(length_of_snake - 1, high_score, level)
        pygame.display.update()

        # Food collision
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            length_of_snake += 1
            try:
                eat_sound.play()
            except:
                pass

            if length_of_snake % 5 == 0:
                level += 1
                speed += 2

        if length_of_snake - 1 > high_score:
            high_score = length_of_snake - 1
            save_high_score(high_score)

        clock.tick(speed)

    pygame.quit()

# Run the game
game_loop()
