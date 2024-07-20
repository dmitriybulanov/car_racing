import os
import sys
import pygame
from pygame import mixer
from pygame.locals import *
import random
from Player import Player
from Vehicle import Vehicle
from constants import *


# функция загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Игра в "Такси"',
                  "Заработай как можно больше",
                  "денег за свой заказ,",
                  "или начни новый:("]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# точка входа в программу
if __name__ == '__main__':
    lane_marker_move_y = 0
    flag_game = False
    speed = 2
    money = 0
    # группы спрайтов
    player_group = pygame.sprite.Group()
    vehicle_group = pygame.sprite.Group()
    player = Player(PLAYER_X, PLAYER_Y)
    player_group.add(player)

    # загрузка спрайтов
    image_filenames = ['taxi_ub.png', 'truck_maks.png', 'van_mobil.png']
    vehicle_images = []
    for im in image_filenames:
        image = pygame.image.load('data/' + im)
        vehicle_images.append(image)
    boom = pygame.image.load('data/boom.png')
    boom_rect = boom.get_rect()
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    # загрузка музыки, иконки итд.
    pygame.display.set_caption('Таксист 2.0')
    icon = pygame.image.load('data/taxi_icon.ico')
    pygame.display.set_icon(icon)
    start_screen()
    mixer.music.load('data/race.wav')
    sound1 = mixer.Sound('data/boom.wav')
    # игровой цикл
    running = True
    mixer.music.play(-1)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # управление игрока
            if event.type == KEYDOWN:
                if event.key == K_LEFT and player.rect.center[0] > LEFT_LANE:
                    player.rect.x -= 100
                elif event.key == K_RIGHT and player.rect.center[0] < RIGHT_LANE:
                    player.rect.x += 100
                # проверка столкновения
                for vehicle in vehicle_group:
                    if pygame.sprite.collide_rect(player, vehicle):
                        flag_game = True
                        # обработка взрыва
                        if event.key == K_LEFT:
                            player.rect.left = vehicle.rect.right
                            boom_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                        elif event.key == K_RIGHT:
                            player.rect.right = vehicle.rect.left
                            boom_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

        # рисуем дорогу, траву
        screen.fill(GREEN)
        pygame.draw.rect(screen, GRAY, road)
        pygame.draw.rect(screen, YELLOW, left_edge_marker)
        pygame.draw.rect(screen, YELLOW, right_edge_marker)
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= LINE_HEIGHT * 2:
            lane_marker_move_y = 0
        for y in range(LINE_HEIGHT * -2, HEIGHT, LINE_HEIGHT * 2):
            pygame.draw.rect(screen, WHITE, (LEFT_LANE + 45, y + lane_marker_move_y, LINE_WIDTH, LINE_HEIGHT))
            pygame.draw.rect(screen, WHITE, (CENTER_LANE + 45, y + lane_marker_move_y, LINE_WIDTH, LINE_HEIGHT))

        player_group.draw(screen)
        # добавление случайной  машины, если это возможно
        if len(vehicle_group) < 2:
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False
            if add_vehicle:
                lane = random.choice(lanes)
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, HEIGHT / -2)
                vehicle_group.add(vehicle)
        for vehicle in vehicle_group:
            vehicle.rect.y += speed

            # удаление машины за пределами дороги
            if vehicle.rect.top >= HEIGHT:
                vehicle.kill()
                # увеличиваем баланс поездки и скорость
                money += random.randint(1, 10)
                if money > 0 and money % 5 == 0:
                    speed += 1
        vehicle_group.draw(screen)

        # выводим статистику стоимости поездки
        font = pygame.font.Font(pygame.font.get_default_font(), 15)
        text = font.render('Цена заказа: ', True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (50, 25)
        screen.blit(text, text_rect)
        text = font.render(str(money) + ' руб.', True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (55, 45)
        screen.blit(text, text_rect)

        if pygame.sprite.spritecollide(player, vehicle_group, True):
            sound1.play()
            flag_game = True
            boom_rect.center = [player.rect.center[0], player.rect.top]

        # обработка проигрыша
        if flag_game:
            screen.blit(boom, boom_rect)
            pygame.draw.rect(screen, BLUE, (0, 70, WIDTH, 75))
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text = font.render('Провалено. Взять еще один заказ? (нажми Y или N)', True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH / 2, 100)
            screen.blit(text, text_rect)

        pygame.display.update()
        while flag_game:
            mixer.music.stop()
            clock.tick(FPS)
            # обработка действия пользователя после проигрыша
            for event in pygame.event.get():
                if event.type == QUIT:
                    flag_game = False
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        mixer.music.play(-1)
                        flag_game = False
                        speed = 2
                        money = 0
                        vehicle_group.empty()
                        player.rect.center = [PLAYER_X, PLAYER_Y]
                    elif event.key == K_n:
                        flag_game = False
                        running = False
    pygame.quit()
