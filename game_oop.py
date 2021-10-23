import pygame
from os import path
import random
import ctypes
from math import *

# Описание классов
# Клетки

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.numbx = int((self.x-Width_empty)//Cells_edge)
        self.numby = int((self.y-Height_empty)//Cells_edge)
        self.ontop = 0  # Объект находящийся на клетке. Равен нулю, в случае его отсутствия

class Grass(Cell):
    def __init__(self, x, y):
        Cell.__init__(self, x, y)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле.jpg")), (Cells_edge, Cells_edge))
        self.rect = self.image.get_rect()
        self.rect.center = (x+Cells_edge//2, y+Cells_edge//2)
        self.activated = False
    def activate(self):
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_Активированное.jpg")), (Cells_edge, Cells_edge))
        self.activated = True
    def deactivate(self):
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле.jpg")), (Cells_edge, Cells_edge))
        self.activated = False
    def attack_activate(self):
        if self.ontop.color == "Red":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_Синее.jpg")), (Cells_edge, Cells_edge))
            self.activated = True
        elif self.ontop.color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_Красное.jpg")), (Cells_edge, Cells_edge))
            self.activated = True
        else:
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_активированное_атака")),
                                                (Cells_edge, Cells_edge))
            self.activated = False



#Класс базы
class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, player_color):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.color=player_color
        if self.color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "База_синяя.png")), (Cells_edge*2-Cells_edge//10, Cells_edge*2-Cells_edge//10))
            self.cells = [field[number_cells_height-3][number_cells_width-4], field[number_cells_height-4][number_cells_width-4], field[number_cells_height-4][number_cells_width-3], field[number_cells_height-3][number_cells_width-3]]
        else:
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "База_красная.png")), (Cells_edge * 2 - Cells_edge // 10, Cells_edge * 2 - Cells_edge // 10))
            self.cells = [field[2][2], field[2][3], field[3][2], field[3][3]]
        self.MaxHealth = 1000
        self.health = 1000
        self.rect=self.image.get_rect()
        self.rect.center=(self.x, self.y)

    def is_destroyed(self): #Функция проверки разрушенности базы. Возвращает истину, в случае , если база разрушена
        if not self.health>0:
            return (True)
        return (False)


#Полоски здоровья
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color=color

class Base_HealthBar(HealthBar):
    def __init__(self, color, base):
        HealthBar.__init__(self, color)
        self.base = base
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
            if self.base.health<0:
                self.base.health=0
            self.image=pygame.transform.scale(self.image,(self.fullwidth-self.fullwidth*(self.base.MaxHealth-self.base.health)//self.base.MaxHealth, self.rect.height))
            self.rect=self.image.get_rect(center=((Width_empty+Cells_edge*5-self.fullwidth*(self.base.MaxHealth-self.base.health)//self.base.MaxHealth//2), (Height_empty - Cells_edge * 1.5)))
        else:
            if self.base.health < 0:
                self.base.health = 0
            self.image = pygame.transform.scale(self.image, (self.fullwidth - self.fullwidth * (self.base.MaxHealth - self.base.health) // self.base.MaxHealth, self.rect.height))
            self.rect = self.image.get_rect(center=(Width - (Width_empty + Cells_edge * 5 - self.fullwidth * (self.base.MaxHealth - self.base.health) // self.base.MaxHealth // 2), Height - (Height_empty - Cells_edge * 1.5)))

class Unit_HealthBar(HealthBar):
    def __init__(self, color, unit):
        HealthBar.__init__(self, color)
        self.unit = unit
        self.height = Cells_edge//6
        self.width = Cells_edge-2
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center=(self.unit.rect.center[0], self.unit.rect.top - Cells_edge//10))
        if self.color == "Red":
            self.image.fill(RED)
        elif self.color == "Blue":
            self.image.fill(BLUE)

    def update(self):
        if self.unit.health<0:
            self.unit.health=0
        self.image = pygame.transform.scale(self.image, (self.width*self.unit.health//self.unit.MaxHealth, self.height))
        self.rect = self.image.get_rect(center=(self.unit.rect.center[0], self.unit.rect.top - Cells_edge//10))


#Юниты
class Unit(pygame.sprite.Sprite):
    def __init__(self, cell, color):
        pygame.sprite.Sprite.__init__(self)
        self.health = 0
        self.MaxHealth = 0
        self.cell = cell
        self.cell.ontop=self
        self.cost = 0
        self.attack_radius = 0
        self.walk_radius = 0
        self.damage = 0
        self.color = color
        self.attack_line = []

    def update(self):
        self.HPbar.update()
        self.rect = self.image.get_rect(center=self.cell.rect.center)

    def activate(self):
        attack_cells = [[] for _ in range(number_cells_height)] # Координаты точек, с верхней клетки по часовой стрелке
        for i in field:
            for j in i:
                if sqrt((j.rect.center[0] - self.rect.center[0])**2 + (j.rect.center[1] - self.rect.center[1])**2) < self.attack_radius*Cells_edge:
                    if j.ontop !=0:
                        if j.ontop.color != self.color:
                            j.attack_activate()
                            activated_cells[2].append(j)
                    attack_cells[j.numby].append(j)

                if sqrt((j.rect.center[0] - self.rect.center[0]) ** 2 + (j.rect.center[1] - self.rect.center[1]) ** 2) < self.walk_radius * Cells_edge:
                    if j.ontop == 0:
                        j.activate()
                        activated_cells[1].append(j)

        activated_cells[0].append(self.cell)

        attack_line=[[], [], [], []]

        for i in attack_cells[:self.cell.numby:]:
            if len(i) != 0:
                attack_line[0].append(i[0])
                attack_line[1].append(i[-1])


        for i in attack_cells[self.cell.numby::]:
            if len(i) != 0:
                attack_line[2].append(i[-1])
                attack_line[3].append(i[0])



        attack_line[0] = sorted(attack_line[0][::-1], key=lambda x: x.numbx)
        attack_line[1] = sorted(attack_line[1], key=lambda x: x.numbx)
        attack_line[2] = sorted(attack_line[2], key=lambda x: x.numbx, reverse=True)
        attack_line[3] = sorted(attack_line[3][::-1], key=lambda x: x.numbx, reverse=True)
        attack_line_points = [[], []]

        for i in attack_line[0]:
            attack_line_points[0].append((i.rect.left, i.rect.bottom))
            attack_line_points[0].append((i.rect.left, i.rect.top))

        for i in attack_line[1]:
            attack_line_points[0].append((i.rect.right, i.rect.top))
            attack_line_points[0].append((i.rect.right, i.rect.bottom))

        for i in attack_line[2]:
            attack_line_points[1].append((i.rect.right, i.rect.top))
            attack_line_points[1].append((i.rect.right, i.rect.bottom))

        for i in attack_line[3]:
            attack_line_points[1].append((i.rect.left, i.rect.bottom))
            attack_line_points[1].append((i.rect.left, i.rect.top))

        self.attack_line= attack_line_points[0] + attack_line_points[1]

    def deactivate(self):
        for i in activated_cells:
            for j in i:
                j.deactivate()
        activated_cells[0], activated_cells[1], activated_cells[2] = [], [], []
        self.attack_line=[]

    def is_destroyed(self):
        if self.health <= 0:
            self.cell.ontop = 0
            self.kill()
            return True
        return False

class Footman(Unit):
    def __init__(self, cell, color):
        Unit.__init__(self, cell, color)
        self.MaxHealth = 100
        self.health = 100
        self.cost = 10
        self.attack_radius = 5
        self.damage = 30
        self.walk_radius = 10
        if color == "Red":
            self.image=pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/red_footman.png")), (Cells_edge-1, Cells_edge-1))
        elif color == "Blue":
            self.image=pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/blue_footman.png")), (Cells_edge-1, Cells_edge-1))
        self.rect = self.image.get_rect(center=self.cell.rect.center)
        self.HPbar = Unit_HealthBar(color, self)
        all_sprites.add(self.HPbar)

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
    for i in Base_red.cells:
        i.ontop=Base_red
    for i in Base_blue.cells:
        i.ontop = Base_blue
    #Полоски здоровья
    Base_red_HealthBar = Base_HealthBar("Red", Base_red)
    Base_blue_HealthBar = Base_HealthBar("Blue", Base_blue)
    all_sprites.add(Base_red_HealthBar, Base_blue_HealthBar)

def Game_Initialize():
    # Инициализация
    global clock
    global screen
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Размеры поля: {number_cells_width} на {number_cells_height} клеток")

def Draw_Screen(screen):
    # Отрисовка поля
    field_sprites.draw(screen)
    all_sprites.draw(screen)
    bases.draw(screen)
    units_red_sprites.draw(screen)
    units_blue_sprites.draw(screen)

    if len(activated_cells[0]) != 0:
        if len(activated_cells[0][0].ontop.attack_line) != 0:
            pygame.draw.lines(screen, WHITE, True, activated_cells[0][0].ontop.attack_line)

    pygame.display.flip()

def swap_color():
    global CurrentColor
    if CurrentColor=="Red":
        CurrentColor="Blue"
    else:
        CurrentColor="Red"
    if len(activated_cells[0]) != 0:
        activated_cells[0][0].ontop.deactivate()

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
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
Field_GREEN = (0,32,0)
#Путь к директории с картинками
img_dir=path.join(path.dirname(__file__), "Resources")

all_sprites = pygame.sprite.Group()
bases = pygame.sprite.Group()
units_red = []
units_blue = []
units_red_sprites = pygame.sprite.Group()
units_blue_sprites = pygame.sprite.Group()

Field_Create()
Game_Initialize()

CurrentColor="Red"

# Игровой цикл
buying_running = True
game_running = False
exit_menu_running = False

activated_cells = [[], [], []]

# Стадия закупки
while buying_running:
    clock.tick(FPS)
    screen.fill(Field_GREEN)

    field_sprites.update()
    all_sprites.update()
    units_red_sprites.update()
    units_blue_sprites.update()

    Draw_Screen(screen)

    # Проверка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:  # Проверка закрытия окна
            buying_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1: # Проверка нажатия левой кнопки мыши
                if exit_button.rect.collidepoint(pygame.mouse.get_pos()):  # Проверка нажатия на кнопку выхода
                    buying_running = False

            if event.button == 3:  # Проверка нажатия правой кнопки мыши
                for i in range(len(field_sprites)):
                    if field[i // number_cells_width][i % number_cells_width].rect.collidepoint(pygame.mouse.get_pos()): #Постановка юнитов
                        if field[i // number_cells_width][i % number_cells_width].ontop == 0:
                            if CurrentColor == "Red":
                                units_red.append(Footman(field[i // number_cells_width][i % number_cells_width], CurrentColor))
                                units_red_sprites.add(units_red[-1])
                                field[i // number_cells_width][i % number_cells_width].ontop = units_red[-1]
                            else:
                                units_blue.append(Footman(field[i // number_cells_width][i % number_cells_width], CurrentColor))
                                units_blue_sprites.add(units_blue[-1])
                                field[i // number_cells_width][i % number_cells_width].ontop = units_blue[-1]
                            swap_color()

                        #else:


# Стадия Игры
while game_running:
    clock.tick(FPS)
    screen.fill(Field_GREEN)

    field_sprites.update()
    all_sprites.update()
    units_red_sprites.update()
    units_blue_sprites.update()

    Draw_Screen(screen)

    #Проверка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT: #Проверка закрытия окна
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN: #Проверка нажатия мыши
            if event.button == 1: #Проверка нажатия левой кнопки
                for i in range(len(field_sprites)):
                    #Активация при нажатии
                    if field[i // number_cells_width][i % number_cells_width].rect.collidepoint(pygame.mouse.get_pos()) and field[i // number_cells_width][i % number_cells_width].ontop != 0:
                        if CurrentColor=="Red" and field[i // number_cells_width][i % number_cells_width].ontop in units_red_sprites:
                            if field[i//number_cells_width][i%number_cells_width] in activated_cells[0]:
                                field[i//number_cells_width][i%number_cells_width].ontop.deactivate()
                            elif len(activated_cells[0]) == 1:
                                activated_cells[0].pop(0).ontop.deactivate()
                                field[i // number_cells_width][i % number_cells_width].ontop.activate()
                            else:
                                field[i // number_cells_width][i % number_cells_width].ontop.activate()

                        if CurrentColor=="Blue" and field[i // number_cells_width][i % number_cells_width].ontop in units_blue_sprites:
                            if field[i//number_cells_width][i%number_cells_width] in activated_cells[0]:
                                field[i//number_cells_width][i%number_cells_width].ontop.deactivate()
                            elif len(activated_cells[0]) == 1:
                                activated_cells[0].pop(0).ontop.deactivate()
                                field[i // number_cells_width][i % number_cells_width].ontop.activate()
                            else:
                                field[i // number_cells_width][i % number_cells_width].ontop.activate()

                if exit_button.rect.collidepoint(pygame.mouse.get_pos()): #Проверка нажатия на кнопку выхода
                    game_running=False
                if Base_red.rect.collidepoint(pygame.mouse.get_pos()):#Урона по базе от нажатия
                    Base_red.health-=random.randint(1,10)*50
                if Base_blue.rect.collidepoint(pygame.mouse.get_pos()):
                    Base_blue.health-=random.randint(1,10)*50

            #Передвижение Юнитов
            if len(activated_cells[0]) != 0:
                if event.button == 1:
                    for i in activated_cells[1]:
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            tUnit=activated_cells[0][0].ontop
                            activated_cells[0][0].ontop = 0
                            tUnit.cell=i
                            i.ontop=tUnit
                            tUnit.deactivate()
                            swap_color()
                    if len(activated_cells[2]) != 0:
                        for j in activated_cells[2]:
                            if j.rect.collidepoint(pygame.mouse.get_pos()):
                                j.ontop.health -= activated_cells[0][0].ontop.damage
                                j.ontop.is_destroyed()

                                swap_color()


            if Base_red.is_destroyed(): #Проверка баз на разрушение
                game_running=False
                Winner="Синие"
                exit_menu_running=True
            if Base_blue.is_destroyed():
                game_running=False
                Winner="Красные"
                exit_menu_running=True

#Победное меню
while exit_menu_running:
    clock.tick(FPS)
    screen.fill(Field_GREEN)

    pygame.sprite.Group(exit_button).draw(screen)
    all_sprites.update()

    exit_menu=pygame.Surface((Width // 3, Height // 3))
    exit_menu.fill(BLACK)
    exit_menu_rect=exit_menu.get_rect(center=(Width//2, Height//2))

    congr=pygame.font.SysFont("None", 22).render(f"Победили {Winner}! Поздравляем!", True, (255,255,255))
    congr_rect=congr.get_rect(center=(Width//2, Height//2))

    screen.blit(exit_menu,exit_menu_rect)
    screen.blit(congr, congr_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.QUIT:
                game_running = False
            if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                exit_menu_running = False
pygame.quit()