import pygame
import os

pygame.init()
# Создание игрового окна
fps = 3
width, height = 1000, 600
start = [150, 472]
end = [230, 472]
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
        self.rect.x, self.rect.y = start
        self.rect.y -= 15

    def update(self, *args):
        self.rect.x += 80
        self.rect.y += end[1] - 472


class guns(pygame.sprite.Sprite):
    image = load_image("gun.png")
    image = pygame.transform.smoothscale(image, (150, 150))

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = guns.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 450




pygame.display.set_caption("Игра")
all_sprites = pygame.sprite.Group()
gun = guns(all_sprites)
group_safety = pygame.sprite.Group()
group_gunshot = pygame.sprite.Group()
group_gun = pygame.sprite.Group()
group_gun.add(gun)
safety_x = 160
safety_y = 550
for i in range(5):
    spr = missile(all_sprites)
    spr.rect.y = safety_y
    spr.rect.x = safety_x
    group_safety.add(spr)
    safety_x += 32

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
                if len(group_gunshot) == 0:
                    end[1] += 5

            if event.key == pygame.K_UP:
                if len(group_gunshot) == 0:
                    end[1] -= 5

            if event.key == pygame.K_SPACE:
                group_gunshot.add(missile(group_gunshot))

    for spr in group_gunshot:
        if spr.rect.x > 1000 or spr.rect.x < 0 or spr.rect.y > 600 or spr.rect.y < 0:
            group_gunshot.remove(spr)






    # Очистка окна
    game_window.fill((255, 255, 255))
    pygame.draw.line(game_window, (255, 0, 0), start, end, thickness)
    group_safety.draw(game_window)
    group_gun.draw(game_window)
    group_gunshot.draw(game_window)
    group_gunshot.update(game_window)



    # Обновление окна
    pygame.display.update()

# Завершение работы Pygame
pygame.quit()