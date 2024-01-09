import pygame

# Инициализация Pygame
pygame.init()

# Создание игрового окна
width, height = 1000, 600
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра")

# Основной цикл игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка окна
    game_window.fill((255, 255, 255))


    # Обновление окна
    pygame.display.update()

# Завершение работы Pygame
pygame.quit()