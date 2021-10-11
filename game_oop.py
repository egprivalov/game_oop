import pygame
from os import path
import ctypes

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

def Field_Create():
    # Создание поля
    global field
    global field_sprites
    global exit_button
    exit_button = pygame.sprite.Sprite()  # Кнопка выхода
    exit_button.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "кнопка_выхода.png")), (30, 30))
    exit_button.rect = exit_button.image.get_rect()
    exit_button.rect.center = (Width - 30, 30)
    all_sprites.add(exit_button)

    field = [[] for _ in range(number_cells_height)] #Клетки поля
    field_sprites = pygame.sprite.Group()
    for i in range(number_cells_height):
        for j in range(number_cells_width):
            field[i].append(Grass(j * Cells_edge + Width_empty, i * Cells_edge + Height_empty))
            field_sprites.add(field[i][j])

def Game_Initialize():
    # Инициализация
    global clock
    global screen
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Размеры поля: {number_cells_width} на {number_cells_height} клеток")

#Константы
Width=ctypes.windll.user32.GetSystemMetrics(0)
Height=ctypes.windll.user32.GetSystemMetrics(1)
Width_empty=int(Width*0.1) + 5 #Отступ от края экрана по ширине
Height_empty=int(Height*0.1) + 6 #Отступ от края экрана по высоте
print(f"Размеры экрана: {Width, Height}")
print(f"Размеры поля: {Width-Width_empty*2, Height-Height_empty*2}")

Cells_edge = 20 #Изменять только на число, которое делит и Width и Height
number_cells_width = (Width - 2*Width_empty) // Cells_edge
number_cells_height = (Height - 2*Height_empty) // Cells_edge
print(f"Размеры поля: {number_cells_width} на {number_cells_height} клеток")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (33, 0, 66)
YELLOW = (255, 255, 0)
Field_GREEN = (0,32,0)

img_dir=path.join(path.dirname(__file__), "Resources")

all_sprites = pygame.sprite.Group()

Field_Create()
Game_Initialize()

# Игровой цикл
running = True
while running:
    clock.tick(FPS)
    screen.fill(Field_GREEN)

    field_sprites.update()
    all_sprites.update()

    #Отрисовка поля
    field_sprites.draw(screen)
    all_sprites.draw(screen)
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
            if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                running=False
pygame.quit()