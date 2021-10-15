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
        self.ontop = 0 #Объект находящийся на клетке. Равен нулю, в случае его отсутствия
    def put_ontop(self, object):
        if self.ontop != 0:
            self.ontop=object
        else:
            print("Нi можливо покладати")

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

#Класс базы
class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, player_color):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.color=player_color
        if self.color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "База_синяя.png")), (Cells_edge*2-Cells_edge//10, Cells_edge*2-Cells_edge//10))
        else:
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "База_красная.png")), (Cells_edge * 2 - Cells_edge // 10, Cells_edge * 2 - Cells_edge // 10))
        self.MaxHealth = 1000
        self.health = 1000
        self.rect=self.image.get_rect()
        self.rect.center=(self.x, self.y)
    def is_destroyed(self):
        global running
        if not self.health>0:
            print('Игра окончена')
            running=False

#Полоски здоровья
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, color, base):
        pygame.sprite.Sprite.__init__(self)
        self.base = base
        self.color=color
        if self.color=="Red":
            self.image = pygame.Surface((Cells_edge * 10, Cells_edge))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = ((Width_empty+Cells_edge*5), (Height_empty - Cells_edge * 1.5))
            self.fullwidth=self.rect.width
        elif self.color == "Blue":
            self.image = pygame.Surface((Cells_edge * 10, Cells_edge))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.center = (Width - (Width_empty + Cells_edge * 5), Height - (Height_empty - Cells_edge * 1.5))
            self.fullwidth=self.rect.width
    def update(self):
        if self.color=="Red":
            self.image=pygame.transform.scale(self.image,(self.fullwidth-self.fullwidth*(self.base.MaxHealth-self.base.health)//self.base.MaxHealth, self.rect.height))
            self.rect=self.image.get_rect(center=((Width_empty+Cells_edge*5-self.fullwidth*(self.base.MaxHealth-self.base.health)//self.base.MaxHealth//2), (Height_empty - Cells_edge * 1.5)))
        else:
            self.image = pygame.transform.scale(self.image, (self.fullwidth - self.fullwidth * (self.base.MaxHealth - self.base.health) // self.base.MaxHealth, self.rect.height))
            self.rect = self.image.get_rect(center=(Width - (Width_empty + Cells_edge * 5 - self.fullwidth * (self.base.MaxHealth - self.base.health) // self.base.MaxHealth // 2), Height - (Height_empty - Cells_edge * 1.5)))

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
    #Базы
    global Base_red, Base_blue, Base_red_HealthBar, Base_blue_HealthBar
    Base_red = Base(Width_empty+Cells_edge*3, Height_empty+Cells_edge*3, "Red")
    Base_blue = Base(Width-(Width_empty+Cells_edge*3), Height-(Height_empty+Cells_edge*3), "Blue")
    bases.add(Base_red)
    bases.add(Base_blue)
    #Полоски здоровья
    Base_red_HealthBar = HealthBar("Red", Base_red)
    Base_blue_HealthBar = HealthBar("Blue", Base_blue)
    all_sprites.add(Base_red_HealthBar, Base_blue_HealthBar)

def Game_Initialize():
    # Инициализация
    global clock
    global screen
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Размеры поля: {number_cells_width} на {number_cells_height} клеток")

def Draw_Screen(screen):
    # Отрисовка поля
    field_sprites.draw(screen)
    all_sprites.draw(screen)
    bases.draw(screen)

    pygame.display.flip()

#Константы
#Размеры экрана
Width=ctypes.windll.user32.GetSystemMetrics(0)
Height=ctypes.windll.user32.GetSystemMetrics(1)
#Количество клеток в строке
number_cells_width = 75
#Количество строк
number_cells_height = 25

Cells_edge = int(Height/1.5/number_cells_height/5)*5 #Сторона клетки

Width_empty = Width // 2 - number_cells_width/2*Cells_edge #Отступ от края экрана по ширине
Height_empty = Height // 2 - number_cells_height/2*Cells_edge  #Отступ от края экрана по высоте
print(f"Размеры экрана: {Width, Height}")
print(f"Размеры поля: {Width-Width_empty*2, Height-Height_empty*2}")
print(f"Размеры поля: {number_cells_width} на {number_cells_height} клеток")
#Кадров в секунду
FPS = 60
#Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (33, 0, 66)
YELLOW = (255, 255, 0)
Field_GREEN = (0,32,0)
#Путь к директории с картинками
img_dir=path.join(path.dirname(__file__), "Resources")

all_sprites = pygame.sprite.Group()
bases = pygame.sprite.Group()

Field_Create()
Game_Initialize()

# Игровой цикл
running = True

while running:
    clock.tick(FPS)
    screen.fill(Field_GREEN)

    field_sprites.update()
    all_sprites.update()

    Draw_Screen(screen)

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
            if Base_red.rect.collidepoint(pygame.mouse.get_pos()):
                Base_red.health-=100
                Base_red.is_destroyed()
            if Base_blue.rect.collidepoint(pygame.mouse.get_pos()):
                Base_blue.health-=100
                Base_blue.is_destroyed()

pygame.quit()