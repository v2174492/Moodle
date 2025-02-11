import pygame
import time
import random
import sys

# Инициализация pygame
pygame.init()

# Новые светлые цвета
background_color = (245, 245, 220)  # Светлый бежевый
snake_color = (144, 238, 144)       # Светло-зеленый
food_color = (255, 182, 193)        # Светло-розовый
text_color = (70, 130, 180)         # Стальной синий
button_color = (173, 216, 230)      # Светло-голубой

# Размеры окна (увеличили)
width = 800  # Ширина увеличена
height = 600  # Высота увеличена

# Создание окна
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')

# Часы для управления скоростью игры
clock = pygame.time.Clock()

# Размер блока змейки
block_size = 20

# Шрифты (используем "компьютерный" шрифт)
font_style = pygame.font.SysFont("Consolas", 25)
score_font = pygame.font.SysFont("Consolas", 35)
menu_font = pygame.font.SysFont("Consolas", 40)

# Функция для отображения счета
def display_score(score):
    value = score_font.render(f"Счет: {score}", True, text_color)
    game_window.blit(value, [10, 10])

# Функция для отрисовки змейки
def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(game_window, snake_color, [block[0], block[1], block_size, block_size])

# Функция для отображения сообщений на экране
def message(msg, color, y_offset=0, font=menu_font):
    mesg = font.render(msg, True, color)
    game_window.blit(mesg, [width / 4 - mesg.get_width() / 2, height / 2 - mesg.get_height() / 2 + y_offset])

# Функция для отображения меню
def show_menu():
    menu = True
    while menu:
        game_window.fill(background_color)

        # Разметка для изображения (правая половина экрана)
        pygame.draw.rect(game_window, (200, 200, 200), [width // 2, 0, width // 2, height])  # Серая область для изображения

        # Текст меню (левая половина экрана)
        message("Змейка", text_color, -150)
        message("1. Легкий", text_color, -80)
        message("2. Средний", text_color, -30)
        message("3. Сложный", text_color, 20)
        message("Q. Выход", text_color, 70)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 10  # Легкий уровень
                if event.key == pygame.K_2:
                    return 15  # Средний уровень
                if event.key == pygame.K_3:
                    return 20  # Сложный уровень
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Функция для отображения меню проигрыша
def show_game_over_menu(score):
    game_over = True
    while game_over:
        game_window.fill(background_color)

        # Текст меню проигрыша
        message("Вы проиграли!", text_color, -100)
        message(f"Ваш счет: {score}", text_color, -50)
        message("R - Рестарт", text_color, 0)
        message("M - Меню", text_color, 50)
        message("Q - Выход", text_color, 100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_m:
                    return "menu"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Основной игровой цикл
def game_loop(snake_speed):
    game_over = False
    game_close = False

    # Начальные координаты змейки
    x = width / 2
    y = height / 2

    # Изменение координат
    x_change = 0
    y_change = 0

    # Змейка и ее длина
    snake_list = []
    snake_length = 1

    # Координаты еды
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:
        while game_close:
            action = show_game_over_menu(snake_length - 1)
            if action == "restart":
                game_loop(snake_speed)
            elif action == "menu":
                snake_speed = show_menu()
                game_loop(snake_speed)
            elif action == "quit":
                game_over = True
                game_close = False

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

        # Проверка на выход за границы
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        game_window.fill(background_color)
        pygame.draw.rect(game_window, food_color, [food_x, food_y, block_size, block_size])

        # Голова змейки
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка на столкновение с собой
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(block_size, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        # Проверка на поедание еды
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

# Запуск меню и игры
snake_speed = show_menu()
game_loop(snake_speed)