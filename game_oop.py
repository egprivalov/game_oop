import pygame
from os import path
import ctypes
from math import *


# Описание классов
# Клетки

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.numbx = int((self.x - Width_empty) // Cells_edge)
        self.numby = int((self.y - Height_empty) // Cells_edge)
        self.ontop = 0  # Объект находящийся на клетке. Равен нулю, в случае его отсутствия


class Grass(Cell):
    def __init__(self, x, y):
        Cell.__init__(self, x, y)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле.jpg")), (Cells_edge, Cells_edge))
        self.rect = self.image.get_rect()
        self.rect.center = (x + Cells_edge // 2, y + Cells_edge // 2)
        self.activated = False

    def activate(self):
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_Активированное.jpg")),
                                            (Cells_edge, Cells_edge))
        self.activated = True

    def deactivate(self):
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле.jpg")), (Cells_edge, Cells_edge))
        self.activated = False

    def attack_activate(self):
        if self.ontop.color == "Red":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_Синее.jpg")),
                                                (Cells_edge, Cells_edge))
            self.activated = True
        elif self.ontop.color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_Красное.jpg")),
                                                (Cells_edge, Cells_edge))
            self.activated = True
        else:
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Поле_активированное_атака")),
                                                (Cells_edge, Cells_edge))
            self.activated = False


class Unit_Cell(pygame.sprite.Sprite):
    def __init__(self, unit, numb):
        global screen
        pygame.sprite.Sprite.__init__(self)
        basecenter = ((Width_empty + Cells_edge * 12), (Height_empty - Cells_edge * 2))
        self.edge = Cells_edge*2
        self.numb = numb
        cent = (basecenter[0] + numb * (self.edge + 2), basecenter[1])
        self.unit = unit
        self.image = pygame.transform.scale(unit.image, (self.edge, self.edge))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = cent
        self.color = (120, 120, 120)
        self.activated = False

    def update(self):
        if CurrentColor != self.unit.color and buying_running:
            self.unit = units_false[CurrentColor][self.numb]
            self.image = pygame.transform.scale(self.unit.image, (self.edge, self.edge))

    def activate(self):
        if not self.activated:
            for i in unit_cells:
                if i.activated:
                    i.activate()
            self.color = (50, 50, 50)
            self.activated = True

        else:
            self.color = (120, 120, 120)
            self.activated = False

    def draw(self, num, rect):
        screen.blit(self.image, rect)




# Класс Игрока
class Player():
    def __init__(self, color):
        self.color = color  # Цвет игрока
        self.money = Start_Money  # Деньги игрока
        self.army = UnitsSpritesByColor[color]  # Армия игрока
        if self.color == "Red":  # База игрока
            self.base = Base(Width_empty + Cells_edge * 3, Height_empty + Cells_edge * 3, "Red")
        else:
            self.base = Base(Width - (Width_empty + Cells_edge * 3), Height - (Height_empty + Cells_edge * 3), "Blue")

    def can_spend(self, amount):
        if self.money - amount >= 0:
            return (True)
        else:
            return (False)

    def spend(self, amount):
        self.money -= amount

    def is_dead(self):
        if self.base.is_destroyed() or len(self.army) == 0:
            return True
        else:
            return False


# Класс базы
class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, player_color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = player_color
        if self.color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "База_синяя.png")),
                                                (Cells_edge * 2 - Cells_edge // 10, Cells_edge * 2 - Cells_edge // 10))
            self.cells = [field[number_cells_height - 3][number_cells_width - 4],
                          field[number_cells_height - 4][number_cells_width - 4],
                          field[number_cells_height - 4][number_cells_width - 3],
                          field[number_cells_height - 3][number_cells_width - 3]]
        else:
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "База_красная.png")),
                                                (Cells_edge * 2 - Cells_edge // 10, Cells_edge * 2 - Cells_edge // 10))
            self.cells = [field[2][2], field[2][3], field[3][2], field[3][3]]
        self.MaxHealth = 1000
        self.health = 1000
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def is_destroyed(self):  # Функция проверки разрушенности базы. Возвращает истину, в случае , если база разрушена
        if not self.health > 0:
            return (True)
        return (False)

    def sell(self):
        pass


# Полоски здоровья
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color


class Base_HealthBar(HealthBar):
    def __init__(self, color, base):
        HealthBar.__init__(self, color)
        self.base = base
        if self.color == "Red":
            self.image = pygame.Surface((Cells_edge * 10, Cells_edge))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = ((Width_empty + Cells_edge * 5), (Height_empty - Cells_edge * 1.5))
            self.fullwidth = self.rect.width
        elif self.color == "Blue":
            self.image = pygame.Surface((Cells_edge * 10, Cells_edge))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.center = (Width - (Width_empty + Cells_edge * 5), Height - (Height_empty - Cells_edge * 1.5))
            self.fullwidth = self.rect.width

    def update(self):
        if self.color == "Red":
            if self.base.health < 0:
                self.base.health = 0
            self.image = pygame.transform.scale(self.image, (
            self.fullwidth - self.fullwidth * (self.base.MaxHealth - self.base.health) // self.base.MaxHealth,
            self.rect.height))
            self.rect = self.image.get_rect(center=((Width_empty + Cells_edge * 5 - self.fullwidth * (
                        self.base.MaxHealth - self.base.health) // self.base.MaxHealth // 2),
                                                    (Height_empty - Cells_edge * 1.5)))
        else:
            if self.base.health < 0:
                self.base.health = 0
            self.image = pygame.transform.scale(self.image, (
            self.fullwidth - self.fullwidth * (self.base.MaxHealth - self.base.health) // self.base.MaxHealth,
            self.rect.height))
            self.rect = self.image.get_rect(center=(Width - (Width_empty + Cells_edge * 5 - self.fullwidth * (
                        self.base.MaxHealth - self.base.health) // self.base.MaxHealth // 2),
                                                    Height - (Height_empty - Cells_edge * 1.5)))


class Unit_HealthBar(HealthBar):
    def __init__(self, color, unit):
        HealthBar.__init__(self, color)
        self.unit = unit
        self.height = Cells_edge // 6
        self.width = Cells_edge - 2
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center=(self.unit.rect.center[0], self.unit.rect.top - Cells_edge // 5))
        if self.color == "Red":
            self.image.fill(RED)
        elif self.color == "Blue":
            self.image.fill(BLUE)

    def update(self):
        if self.unit.health < 0:
            self.unit.health = 0
        self.image = pygame.transform.scale(self.image,
                                            (self.width * self.unit.health // self.unit.MaxHealth, self.height))
        self.rect = self.image.get_rect(center=(self.unit.rect.center[0], self.unit.rect.top - Cells_edge // 10))


# Юниты
class Unit(pygame.sprite.Sprite):
    def __init__(self, cell, color):
        pygame.sprite.Sprite.__init__(self)
        self.health = 0
        self.MaxHealth = 0
        self.cell = cell
        self.cell.ontop = self
        self.cost = 0
        self.attack_radius = 0
        self.walk_radius = 0
        self.damage = 0
        self.color = color
        self.HPbar = pygame.sprite.Sprite()
        self.attack_line = []
        self.initiative = 0

    def update(self):
        self.HPbar.update()
        self.rect = self.image.get_rect(center=self.cell.rect.center)

    def activate(self):
        attack_cells = [[] for _ in range(number_cells_height)]  # Координаты точек, с верхней клетки по часовой стрелке
        for i in field:
            for j in i:
                if sqrt((j.rect.center[0] - self.rect.center[0]) ** 2 + (
                        j.rect.center[1] - self.rect.center[1]) ** 2) < self.attack_radius * Cells_edge:
                    if j.ontop != 0:
                        if j.ontop.color != self.color:
                            j.attack_activate()
                            activated_cells[2].append(j)
                    attack_cells[j.numby].append(j)

                if sqrt((j.rect.center[0] - self.rect.center[0]) ** 2 + (
                        j.rect.center[1] - self.rect.center[1]) ** 2) < self.walk_radius * Cells_edge:
                    if j.ontop == 0:
                        j.activate()
                        activated_cells[1].append(j)

        activated_cells[0].append(self.cell)

        attack_line = [[], [], [], []]

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

        self.attack_line = attack_line_points[0] + attack_line_points[1]

    def deactivate(self):
        for i in activated_cells:
            for j in i:
                j.deactivate()
        activated_cells[0], activated_cells[1], activated_cells[2] = [], [], []
        self.attack_line = []

    def is_destroyed(self):
        if self.health <= 0:
            self.cell.ontop = 0
            self.kill()
            return True
        return False

    def sell(self):
        PlayerByColor[CurrentColor].money += self.cost
        self.cell.ontop = 0
        self.HPbar.kill()
        self.kill()


class Soldier(Unit):  # Название класса поменяй, в остальном-все также
    def __init__(self, cell, color):  # Ниче не меняй
        Unit.__init__(self, cell, color) # Ниче не меняй
        # Вот этот блок-трогай
        self.MaxHealth = 250  # Полное здоровье
        self.health = 250  # Текущее здоровье
        self.cost = 100  # Стоимость
        self.attack_radius = 4  # Радиус атаки
        self.damage = 75  # Урон
        self.walk_radius = 4  # Радиус ходьбы
        self.initiative = 10  # Инициатива
        self.name = "Soldier"  # Название юнита

        #Лучше не трогать, просто оставь, потом скинешь текстуры
        if color == "Red":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/Red_Soldier.png")), (Cells_edge - 1, Cells_edge - 1))
        elif color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/Blue_Soldier.png")), (Cells_edge - 1, Cells_edge - 1))
        #Вообще не трогай
        self.rect = self.image.get_rect(center=self.cell.rect.center)
        self.HPbar = Unit_HealthBar(color, self)

        all_sprites.add(self.HPbar)

class Tank(Unit):
    def __init__(self, cell, color):  # Ниче не меняй
        Unit.__init__(self, cell, color)  # Ниче не меняй
        # Вот этот блок-трогай
        self.MaxHealth = 500  # Полное здоровье
        self.health = 500  # Текущее здоровье
        self.cost = 450  # Стоимость
        self.attack_radius = 2  # Радиус атаки
        self.damage = 250  # Урон
        self.walk_radius = 5  # Радиус ходьбы
        self.initiative = 1  # Инициатива
        self.name = "Tank"  # Название юнита

        # Лучше не трогать, просто оставь, потом скинешь текстуры
        if color == "Red":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/Red_Tank.png")),
                                                (Cells_edge - 1, Cells_edge - 1))
        elif color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/Blue_Tank.png")),
                                                (Cells_edge - 1, Cells_edge - 1))
        # Вообще не трогай
        self.rect = self.image.get_rect(center=self.cell.rect.center)
        self.HPbar = Unit_HealthBar(color, self)

        all_sprites.add(self.HPbar)

class Sniper(Unit):  # Название класса поменяй, в остальном-все также
    def __init__(self, cell, color):  # Ниче не меняй
        Unit.__init__(self, cell, color)  # Ниче не меняй
        # Вот этот блок-трогай
        self.MaxHealth = 100  # Полное здоровье
        self.health = 100  # Текущее здоровье
        self.cost = 250  # Стоимость
        self.attack_radius = 15  # Радиус атаки
        self.damage = 200  # Урон
        self.walk_radius = 4  # Радиус ходьбы
        self.initiative = 5  # Инициатива
        self.name = "Sniper"  # Название юнита

        # Лучше не трогать, просто оставь, потом скинешь текстуры
        if color == "Red":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/Red_Sniper.png")),
                                                (Cells_edge - 1, Cells_edge - 1))
        elif color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/Blue_Sniper.png")),
                                                (Cells_edge - 1, Cells_edge - 1))
        # Вообще не трогай
        self.rect = self.image.get_rect(center=self.cell.rect.center)
        self.HPbar = Unit_HealthBar(color, self)

        all_sprites.add(self.HPbar)

class Bombarda(Unit):
    def __init__(self, cell, color):  # Ниче не меняй
        Unit.__init__(self, cell, color)  # Ниче не меняй
        # Вот этот блок-трогай
        self.MaxHealth = 200  # Полное здоровье
        self.health = 200  # Текущее здоровье
        self.cost = 350  # Стоимость
        self.attack_radius = 7  # Радиус атаки
        self.damage = 300  # Урон
        self.walk_radius = 2  # Радиус ходьбы
        self.initiative = 2  # Инициатива
        self.name = "Bombarda"  # Название юнита

        # Лучше не трогать, просто оставь, потом скинешь текстуры
        if color == "Red":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/Red_Bombarda.png")),
                                                (Cells_edge - 1, Cells_edge - 1))
        elif color == "Blue":
            self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Units/Blue_Bombarda.png")),
                                                (Cells_edge - 1, Cells_edge - 1))
        # Вообще не трогай
        self.rect = self.image.get_rect(center=self.cell.rect.center)
        self.HPbar = Unit_HealthBar(color, self)

        all_sprites.add(self.HPbar)

def CreateUnit(cell):
    if CurrentUnit == "Soldier":
        tunit = Soldier(cell, CurrentColor)
    elif CurrentUnit == "Tank":
        tunit = Tank(cell, CurrentColor)
    elif CurrentUnit == "Sniper":
        tunit = Sniper(cell, CurrentColor)
    elif CurrentUnit == "Bombarda":
        tunit = Bombarda(cell, CurrentColor)
    UnitsSpritesByColor[CurrentColor].add(tunit)
    cell.ontop = tunit
    PlayerByColor[CurrentColor].spend(tunit.cost)


def fightqueueCreate():
    unred = list(units_red_sprites)
    unblue = list(units_blue_sprites)
    while len(unred) != 0 or len(unblue) != 0:
        if len(unred) != 0:
            FightQueue.add(unred.pop(0))
        if len(unblue) != 0:
            FightQueue.add(unblue.pop(0))


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

    field = [[] for _ in range(number_cells_height)]  # Клетки поля
    field_sprites = pygame.sprite.Group()
    for i in range(number_cells_height):
        for j in range(number_cells_width):
            field[i].append(Grass(j * Cells_edge + Width_empty, i * Cells_edge + Height_empty))
            field_sprites.add(field[i][j])
    # Игроки
    global Player_Red, Player_Blue, Bases
    # Красный игрок
    Player_Red = Player("Red")
    # Синий игрок
    Player_Blue = Player("Blue")

    Player_Red.base = Base(Width_empty + Cells_edge * 3, Height_empty + Cells_edge * 3, "Red")
    Player_Blue.base = Base(Width - (Width_empty + Cells_edge * 3), Height - (Height_empty + Cells_edge * 3), "Blue")

    Bases = pygame.sprite.Group()
    Bases.add(Player_Red.base, Player_Blue.base)

    # Массив игроков
    Players = [Player_Red, Player_Blue]
    for i in Players:
        for j in i.base.cells:
            j.ontop = i.base

    # Полоски здоровья
    Base_red_HealthBar = Base_HealthBar("Red", Player_Red.base)
    Base_blue_HealthBar = Base_HealthBar("Blue", Player_Blue.base)
    all_sprites.add(Base_red_HealthBar, Base_blue_HealthBar)

    # Кнопка подтверждения
    global Confirm_button
    Confirm_button = pygame.sprite.Sprite()
    Confirm_button.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "Кнопка подтверждения.jpg")),
                                                  (Cells_edge * 5, Cells_edge * 3))
    Confirm_button.rect = Confirm_button.image.get_rect(
        center=(Width - Width_empty - Cells_edge * 2.5, Height_empty - Height_empty // 3))
    all_sprites.add(Confirm_button)

    # Клетки Юнитов
    for i in range(len(units_false[CurrentColor])):
        unit_cells.add(Unit_Cell(units_false[CurrentColor][i], i))


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
    Bases.draw(screen)
    units_red_sprites.draw(screen)
    units_blue_sprites.draw(screen)

    if len(activated_cells[0]) != 0:
        if len(activated_cells[0][0].ontop.attack_line) != 0:
            pygame.draw.lines(screen, WHITE, True, activated_cells[0][0].ontop.attack_line)

    unit_cells.update()

    if buying_running:
        for i in unit_cells:
            pygame.draw.rect(screen, i.color, i.rect)
            pygame.draw.rect(screen, WHITE, i.rect, 1)

        unit_cells.draw(screen)
        font = pygame.font.SysFont("None", 55, True)
        money_print = font.render(str(PlayerByColor[CurrentColor].money), True, YELLOW)
        money_rect = money_print.get_rect(center=(Width - 150, 33))
        screen.blit(money_print, money_rect)

        put_line_red = [(523, 169), (523, 204), (523, 204), (523, 239), (523, 239), (523, 274), (523, 274), (523, 309),
                        (523, 309), (523, 344), (488, 344), (488, 379), (488, 379), (488, 414), (453, 414), (453, 449),
                        (453, 449), (453, 484), (418, 484), (418, 519), (383, 519), (383, 554), (313, 554), (313, 589),
                        (243, 589), (243, 624), (68, 624), (68, 589), (68, 589), (68, 554), (68, 554), (68, 519),
                        (68, 519), (68, 484), (68, 484), (68, 449), (68, 449), (68, 414), (68, 414), (68, 379),
                        (68, 379), (68, 344), (68, 344), (68, 309), (68, 309), (68, 274), (68, 274), (68, 239),
                        (68, 239), (68, 204), (68, 204), (68, 169)]
        put_line_blue = [(1013, 659), (1013, 624), (1013, 624), (1013, 589), (1013, 589), (1013, 554), (1013, 554),
                         (1013, 519), (1048, 519), (1048, 484), (1048, 484), (1048, 449), (1083, 449), (1083, 414),
                         (1083, 414), (1083, 379), (1118, 379), (1118, 344), (1153, 344), (1153, 309), (1223, 309),
                         (1223, 274), (1293, 274), (1293, 239), (1468, 239), (1468, 274), (1468, 274), (1468, 309),
                         (1468, 309), (1468, 344), (1468, 344), (1468, 379), (1468, 379), (1468, 414), (1468, 414),
                         (1468, 449), (1468, 449), (1468, 484), (1468, 484), (1468, 519), (1468, 519), (1468, 554),
                         (1468, 554), (1468, 589), (1468, 589), (1468, 624), (1468, 624), (1468, 659), (1468, 659),
                         (1468, 694), (1013, 694), (1013, 659)]

        if CurrentColor == "Red":
            pygame.draw.lines(screen, RED, True, put_line_red, 3)
        else:
            pygame.draw.lines(screen, BLUE, True, put_line_blue, 3)



    elif game_running:
        queue = list(unit_cells)[start % len(unit_cells)::] + list(unit_cells)[:start % len(unit_cells)]
        for i in range(10):
            if i == 0:
                color = (50, 50, 50)
            else:
                color = (120, 120, 120)
            pygame.draw.rect(screen, color, QueueRects[i])
            queue[i % len(queue)].draw(i, QueueRects[i])

    pygame.display.flip()


def swap_color():
    global CurrentColor
    global CurrentUnit
    if CurrentColor == "Red":
        CurrentColor = "Blue"
    else:
        CurrentColor = "Red"
    CurrentUnit = ""
    for i in unit_cells:
        if i.activated:
            i.activate()
    if len(activated_cells[0]) != 0:
        activated_cells[0][0].ontop.deactivate()


# Константы
# Размеры экрана
Width = ctypes.windll.user32.GetSystemMetrics(0)
Height = ctypes.windll.user32.GetSystemMetrics(1)

# Лучше не трогать
# Количество клеток в строке
number_cells_width = 40
# Количество строк
number_cells_height = 15

Cells_edge = int(Height / 1.5 / number_cells_height / 5) * 5  # Сторона клетки

Width_empty = Width // 2 - number_cells_width / 2 * Cells_edge  # Отступ от края экрана по ширине
Height_empty = Height // 2 - number_cells_height / 2 * Cells_edge  # Отступ от края экрана по высоте
print(f"Размеры экрана: {Width, Height}")
print(f"Размеры поля: {Width - Width_empty * 2, Height - Height_empty * 2}")
print(f"Размеры поля: {number_cells_width} на {number_cells_height} клеток")

# Кадров в секунду
FPS = 60
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
Field_GREEN = (0, 32, 0)

# Путь к директории с картинками
img_dir = path.join(path.dirname(__file__), "Resources")

# Начальное количество денег у игроков
Start_Money = 3000

field = [[Grass(0, 0)]]
CurrentColor = "Red"

all_sprites = pygame.sprite.Group()
units_red_sprites = pygame.sprite.Group()
units_blue_sprites = pygame.sprite.Group()
UnitsSpritesByColor = {"Red": units_red_sprites, "Blue": units_blue_sprites}

# Ложные юниты
units_false = {"Red": [Soldier(field[0][0], "Red"), Tank(field[0][0], "Red"), Sniper(field[0][0], "Red"), Bombarda(field[0][0], "Red")],
               "Blue": [Soldier(field[0][0], "Blue"), Tank(field[0][0], "Blue"), Sniper(field[0][0], "Blue"), Bombarda(field[0][0], "Blue")]}

# Клетки с юнитами
unit_cells = pygame.sprite.Group()

Game_Initialize()
Field_Create()

PlayerByColor = {"Red": Player_Red, "Blue": Player_Blue}
UnitsCosts = {"Soldier": 100, "Tank": 450, "Sniper": 250, "Bombarda": 350}

CurrentUnit = ""

put_field = {
    "Red": {0: 12, 1: 12, 2: 12, 3: 12, 4: 12, 5: 11, 6: 11, 7: 10, 8: 10, 9: 9, 10: 8, 11: 6, 12: 4, 13: 0, 14: 0},
    "Blue": {14: 27, 13: 27, 12: 27, 11: 27, 10: 27, 9: 28, 8: 28, 7: 29, 6: 29, 5: 30, 4: 31, 3: 33, 2: 35, 1: 40, 0: 40}}

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
            if event.button == 1:  # Проверка нажатия левой кнопки мыши
                # Проверка нажатия на кнопку выхода
                if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    buying_running = False

                # Проверка нажатия на кнопку подтверждения
                if Confirm_button.rect.collidepoint(pygame.mouse.get_pos()):
                    if CurrentColor == "Red":
                        swap_color()
                    else:
                        buying_running = False
                        game_running = True
                        Confirm_button.kill()
                        swap_color()
                for i in unit_cells:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        if not i.activated:
                            CurrentUnit = i.unit.name
                            i.activate()
                        else:
                            CurrentUnit = ""
                            i.activate()

            if event.button == 3:  # Проверка нажатия правой кнопки мыши
                for i in field:
                    for j in i:
                        if j.rect.collidepoint(pygame.mouse.get_pos()):  # Постановка юнитов
                            if j.ontop == 0:
                                if (put_field[CurrentColor][j.numby] >= j.numbx and CurrentColor == "Red") or (
                                        put_field[CurrentColor][j.numby] <= j.numbx and CurrentColor == "Blue"):
                                    if CurrentUnit != "":
                                        if PlayerByColor[CurrentColor].can_spend(UnitsCosts[CurrentUnit]):
                                            CreateUnit(j)

                            elif j.ontop.color == CurrentColor:  # Убрать юнита
                                j.ontop.sell()

# Создание Очереди ходов
FightQueue = pygame.sprite.Group()
fightqueueCreate()
FightQueue = sorted(FightQueue, key=lambda x: x.initiative)
QueueRects = []

unit_cells = pygame.sprite.Group()
for i in range(len(FightQueue)):
    unit_cells.add(Unit_Cell(FightQueue[i], i))

for i in range(25):
    QueueRects.append(pygame.Surface((Cells_edge * 2, Cells_edge * 2)).get_rect(
        center=((Width_empty + Cells_edge * 12) + i * (Cells_edge * 2 + 2), (Height_empty - Cells_edge * 2))))

start = 0

if len(FightQueue) == 0:
    game_running = False
    exit_menu_running = True
    Winner = "Оба"

# Стадия Игры
while game_running:
    clock.tick(FPS)
    screen.fill(Field_GREEN)

    field_sprites.update()
    all_sprites.update()
    units_red_sprites.update()
    units_blue_sprites.update()

    if Player_Red.is_dead():  # Проверка На проигрыш
        game_running = False
        Winner = "Синие"
        exit_menu_running = True
    if Player_Blue.is_dead():
        game_running = False
        Winner = "Красные"
        exit_menu_running = True

    while len(activated_cells[0]) == 0:
        uni = FightQueue[start % len(FightQueue)]
        if uni.alive():
            uni.activate()
        else:
            start += 1

    Draw_Screen(screen)

    # Проверка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:  # Проверка закрытия окна
            game_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # Проверка нажатия мыши
            if event.button == 1:  # Проверка нажатия левой кнопки
                if exit_button.rect.collidepoint(pygame.mouse.get_pos()):  # Проверка нажатия на кнопку выхода
                    game_running = False

                # Передвижение Юнитов
                if len(activated_cells[0]) != 0:
                    for i in activated_cells[1]:
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            tUnit = activated_cells[0][0].ontop
                            activated_cells[0][0].ontop = 0
                            tUnit.cell = i
                            i.ontop = tUnit
                            tUnit.deactivate()
                            start += 1

                    if len(activated_cells[2]) != 0:
                        for j in activated_cells[2]:
                            if j.rect.collidepoint(pygame.mouse.get_pos()):
                                j.ontop.health -= activated_cells[0][0].ontop.damage
                                j.ontop.is_destroyed()
                                activated_cells[0][0].ontop.deactivate()
                                start += 1


# Победное меню
while exit_menu_running:
    clock.tick(FPS)
    screen.fill(Field_GREEN)

    pygame.sprite.Group(exit_button).draw(screen)
    all_sprites.update()

    exit_menu = pygame.Surface((Width // 3, Height // 3))
    exit_menu.fill(BLACK)
    exit_menu_rect = exit_menu.get_rect(center=(Width // 2, Height // 2))

    congr = pygame.font.SysFont("None", 22).render(f"Победили {Winner}! Поздравляем!", True, (255, 255, 255))
    congr_rect = congr.get_rect(center=(Width // 2, Height // 2))

    screen.blit(exit_menu, exit_menu_rect)
    screen.blit(congr, congr_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.QUIT:
                game_running = False
            if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                exit_menu_running = False
pygame.quit()
