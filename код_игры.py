import pygame
import os

pygame.init()
# Создание игрового окна
fps = 3
width, height = 1000, 600
start = [40, 500]
end = [100, 500]
thickness = 5
game_window = pygame.display.set_mode((width, height))


def load_image(name, color_key=None):  # Функция для загрузки изображения
    fullname = os.path.join('data', name)  # Путь к файлу изображения
    try:
        image = pygame.image.load(fullname)  # Загружаем изображение
    except pygame.error as message:
        print('Не удаётся загрузить:', name)  # Выводим сообщение об ошибке
        raise SystemExit(message)  # Завершаем работу программы
    image = image.convert_alpha()  # Преобразуем изображение в формат RGBA
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))  # Определяем цвет ключа изображения
        image.set_colorkey(color_key)  # Устанавливаем цвет ключа изображения
    return image


class missile(pygame.sprite.Sprite):
    image = load_image("missile.png")
    image = pygame.transform.smoothscale(image, (30, 30))

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = missile.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = end[1] -15

    def update(self, *args):
        self.rect.x += 60
        self.rect.y += end[1] - 500




pygame.display.set_caption("Игра")
gun = pygame.image.load('data/gun.png')
all_sprites = pygame.sprite.Group()
group_missile = pygame.sprite.Group()
clock = pygame.time.Clock()




# Основной цикл игры
running = True
while running:

    clock.tick(fps)


    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN:
                end[1] += 5

            if event.key == pygame.K_UP:
                end[1] -= 5

            if event.key == pygame.K_SPACE:
                group_missile.add(missile(all_sprites))





    # Очистка окна
    game_window.fill((255, 255, 255))
    pygame.draw.line(game_window, (255, 0, 0), start, end, thickness)
    all_sprites.draw(game_window)
    all_sprites.update(game_window)


    # Обновление окна
    pygame.display.update()

# Завершение работы Pygame
pygame.quit()