import pygame
from os import path

#Описание классов


#Клетки
class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
class Grass(Cell):
    def __init__(self, x, y):
        Cell.__init__(self, x, y)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле.jpg")), (Cells_edge, Cells_edge))
        self.rect = self.image.get_rect()
        self.rect.center = (x+Cells_edge//2, y+Cells_edge//2)
        self.activated=False
    def activate(self):
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_Активированное.jpg")), (Cells_edge, Cells_edge))
        self.activated=True
    def deactivate(self):
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле.jpg")), (Cells_edge, Cells_edge))
        self.activated=False
#Константы
Width=1080
Height=640
FPS = 60

Cells_edge = 20 #Изменять только на число, которое делит и Width и Height
number_cells_width = Width // Cells_edge
number_cells_height = Height // Cells_edge

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (33, 0, 66)
YELLOW = (255, 255, 0)

img_dir=path.join(path.dirname(__file__), "Resources")

all_sprites = pygame.sprite.Group()

#Инициализация
pygame.init()
pygame.mixer.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
pygame.display.set_caption(f"Размеры поля: {number_cells_width} на {number_cells_height} клеток")

#Создание поля
field=[[] for _ in range(number_cells_height)]
field_sprites=pygame.sprite.Group()
for i in range(number_cells_height):
    for j in range(number_cells_width):
        field[i].append(Grass(j*Cells_edge, i*Cells_edge))
        field_sprites.add(field[i][j])

# Игровой цикл
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    field_sprites.update()
    #Отрисовка поля
    field_sprites.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(field_sprites)):
                n = i
                if field[n//number_cells_width][n%number_cells_width].rect.collidepoint(pygame.mouse.get_pos()):
                    if field[n//number_cells_width][n%number_cells_width].activated:
                        field[n//number_cells_width][n%number_cells_width].deactivate()
                    else:
                        field[n // number_cells_width][n % number_cells_width].activate()
pygame.quit()