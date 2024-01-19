import pygame
import os
from random import randint
import sys

pygame.init()
fps = 5
width, height = 1000, 600
start = [150, 472]
end = [230, 472]
thickness = 5
game_window = pygame.display.set_mode((width, height))
start_window = pygame.display.set_mode((500, 400))
level_window = pygame.display.set_mode((600, 200))
end_window = pygame.display.set_mode((400, 300))
count = 0  # количество мишеней
count1 = 0  # количество сбитых мишений


def write_file(file, x):
    with open(file, 'a') as file:
        file.write(str(x) + ' ')


def read_file(file):
    with open(file, 'r') as file:
        array = file.read().strip().split()
        array = list(map(int, array))
    return max(array)


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.display.set_mode((500, 400))
    intro_text = ["Добро пожаловать в игру 'Точный выстрел'",
                  "Прицелься из пушки, нажимая",
                  "клавиши-стрелочки вверх или вниз",
                  "на клавиатуре. Затем нажми на",
                  "пробел, чтобы произвести выстрел.",
                  "Порази как можно больше мишений.",
                  "",
                  "Нажми любую кнопку для выбора",
                  "уровня."]

    fon = pygame.transform.scale(load_image('фон.jpg'), (500, 400))
    start_window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        start_window.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


def level_screen():
    global count
    pygame.display.set_mode((600, 200))
    intro_text = ["Выберите уровень, нажав одну из клавиш:",
                  "'1', '2' и '3'.",
                  "Чем больще числовой индекс уровня,",
                  "тем больше его сложность."]

    fon = pygame.transform.scale(load_image('фон.jpg'), (600, 200))
    level_window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        level_window.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    count = 5
                    game_screen()
                    return
                if event.key == pygame.K_2:
                    count = 10
                    game_screen()
                    return
                if event.key == pygame.K_3:
                    count = 15
                    game_screen()
                    return
        pygame.display.flip()


def game_screen():
    global count1
    pygame.display.set_mode((width, height))

    class missile(pygame.sprite.Sprite):
        image = load_image("missile.png")
        image = pygame.transform.smoothscale(image, (30, 30))

        def __init__(self, group):
            super().__init__(group)
            self.image = missile.image
            self.mask = pygame.mask.from_surface(self.image)
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
            super().__init__(group)
            self.image = guns.image
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = 450

    class target(pygame.sprite.Sprite):
        image = load_image("мишень.png")
        image = pygame.transform.smoothscale(image, (70, 70))

        def __init__(self, group):
            super().__init__(group)
            self.image = target.image
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = randint(600, 930)
            self.rect.y = randint(0, 530)

    pygame.display.set_caption("Игра")
    all_sprites = pygame.sprite.Group()
    gun = guns(all_sprites)
    group_safety = pygame.sprite.Group()
    group_gunshot = pygame.sprite.Group()
    group_gun = pygame.sprite.Group()
    group_target = pygame.sprite.Group()
    group_gun.add(gun)
    safety_x = 160
    safety_y = 550
    for i in range(count):
        spr = missile(all_sprites)
        spr.rect.y = safety_y
        spr.rect.x = safety_x
        group_safety.add(spr)
        safety_x += 32

    while len(group_target) < count:
        target_count = target(all_sprites)
        if len(pygame.sprite.spritecollide(target_count, group_target, False)) == 0:
            group_target.add(target_count)

    clock = pygame.time.Clock()

    running = True
    while running:

        clock.tick(fps)

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
                    if len(group_safety) != 0:
                        group_gunshot.add(missile(group_gunshot))
                    for s in group_safety:
                        group_safety.remove(s)
                        break

        for spr in group_gunshot:
            if spr.rect.x > 1000 or spr.rect.x < 0 or spr.rect.y > 600 or spr.rect.y < 0:
                group_gunshot.remove(spr)

        for spr1 in group_target:
            for spr2 in group_gunshot:
                if pygame.sprite.collide_mask(spr1, spr2):
                    group_gunshot.remove(spr2)
                    group_target.remove(spr1)
        if len(group_target) == 0 or (len(group_safety) == 0 and len(group_gunshot) == 0):
            count1 = count - len(group_target)
            if count == 5:
                write_file('data/статистика/уровень 1', count1)
            if count == 10:
                write_file('data/статистика/уровень 2', count1)

            if count == 15:
                write_file('data/статистика/уровень 3', count1)
            end_screen()
            running = False

        game_window.fill((255, 235, 205))
        pygame.draw.line(game_window, (255, 0, 0), start, end, thickness)
        group_safety.draw(game_window)
        group_gun.draw(game_window)
        group_gunshot.draw(game_window)
        group_gunshot.update(game_window)
        group_target.draw(game_window)
        group_target.update(game_window)

        pygame.display.update()


def end_screen():
    global count
    pygame.display.set_mode((400, 300))
    if count == 5:
        mx = read_file('data/статистика/уровень 1')
    if count == 10:
        mx = read_file('data/статистика/уровень 2')
    if count == 15:
        mx = read_file('data/статистика/уровень 3')

    intro_text = [f"Результат {count1}/{count}",
                  f"Лучший результат {mx}/{count}",
                  "",
                  "Нажмите пробел, чтобы вернуться",
                  "к выбору уровня. Закройте окно,",
                  "если хотите завершить игру."]

    fon = pygame.transform.scale(load_image('фон.jpg'), (400, 300))
    end_window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        end_window.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level_screen()
                    return
        pygame.display.flip()


start_screen()
level_screen()
pygame.quit()

