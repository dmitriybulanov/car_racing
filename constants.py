# размеры окна
WIDTH, HEIGHT = 500, 500
screen_size = (WIDTH, HEIGHT)
# константы цветов
RED = (200, 0, 0)
GREEN = (76, 208, 56)
YELLOW = (255, 232, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
# размеры дороги, линий и координаты дорог
ROAD_WIDTH = 300
LINE_WIDTH, LINE_HEIGHT = 15, 50
LEFT_LANE = 150
CENTER_LANE = 250
RIGHT_LANE = 350
# начальные координаты игрока
PLAYER_X, PLAYER_Y = 250, 400
FPS = 120
lanes = [LEFT_LANE, CENTER_LANE, RIGHT_LANE]
road = (100, 0, ROAD_WIDTH, HEIGHT)
left_edge_marker = (95, 0, LINE_WIDTH, HEIGHT)
right_edge_marker = (395, 0, LINE_WIDTH, HEIGHT)