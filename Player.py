import pygame
from Vehicle import Vehicle


# класс игрока-такси
class Player(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load('data/taxi_ya.png')
        super().__init__(image, x, y)