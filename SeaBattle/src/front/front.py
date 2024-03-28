import pprint

from PyQt6.QtGui import QColor, QMouseEvent
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, \
    QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from screeninfo import get_monitors
from SeaBattle.src.backend.player import Player
from SeaBattle.src.backend.game import Game


NUMBER_OF_COLUMN = 5
NUMBER_OF_ROWS = 5
GLOBAL_STEP = 1

INDENT_X_COFF = 0.05208333333333333333333333333333
INDENT_Y_COFF = 0.09259259259259259259259259259259
monitor = get_monitors()[0]
INDENT_X = int(monitor.width * INDENT_X_COFF)
INDENT_Y = int(monitor.height * INDENT_Y_COFF)

WIDTH_COFF = 0.625
HEIGHT_COFF = 0.55555555555555555555555555555556
WIDTH_X = int(monitor.width * WIDTH_COFF)
HEIGHT_Y = int(monitor.height * HEIGHT_COFF)

WIDTH_BUTTON_X = 50
WIDTH_BUTTON_Y = 50

NAME_WINDOW = 'SeaBattle'

FIELD_1 = 1
FIELD_2 = 2

ASCII_START = 65

FLAG = 0

RED_COLOR = 'red'
BLUE_COLOR = 'blue'
WHITE_COLOR = 'white'
GRAY_COLOR = 'gray'

BUTTON_NAME = ['В БОЙ', 'Поместить часть кораблика',
               'Удалить одну часть кораблика']

BUTTON_COLORS = [QColor(GRAY_COLOR), QColor(BLUE_COLOR)]


class ColorChanger(QWidget):

    # создание оси столбцов
    @staticmethod
    def create_cols(grid_layout):
        for j in range(NUMBER_OF_ROWS):
            label = QLabel(str(j + GLOBAL_STEP))
            grid_layout.addWidget(label, j + GLOBAL_STEP, FLAG)

    # создание оси строк
    @staticmethod
    def create_rows(grid_layout):
        for i in range(NUMBER_OF_COLUMN):
            label = QLabel(chr(ASCII_START + i))
            grid_layout.addWidget(label, FLAG, i + GLOBAL_STEP)

    # =========================================================================
    # создание всех кнопок. // из __init__
    def create_grid(self, grid_layout1, grid_layout2):
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLUMN):
                self.create_button(grid_layout1, i, j, self.change_color,
                                   self.buttons1, FIELD_1)
                self.create_button(grid_layout2, i, j, self.change_color,
                                   self.buttons2, FIELD_2)

    # создание одной кнопки
    @staticmethod
    def create_button(grid_layout, i, j, change_color, buttons, field_number):
        button = QPushButton()
        button.setMaximumSize(WIDTH_BUTTON_X, WIDTH_BUTTON_Y)
        button.setStyleSheet('background-color: blue;')

        button.clicked.connect(lambda _, row=i, col=j, grid_num=field_number:
                               change_color(row, col, grid_num))
        grid_layout.addWidget(button, i + GLOBAL_STEP, j + GLOBAL_STEP)
        buttons.append([button, i, j, '#0000ff'])

    def change_color(self, row, col, grid_num):
        if grid_num == FIELD_1:
            button = self.buttons1[row * NUMBER_OF_COLUMN + col][0]
        else:
            button = self.buttons2[row * NUMBER_OF_COLUMN + col][0]

        if self.critical_points(row, col):
            self.buttons1[row * NUMBER_OF_COLUMN + col][3] \
                = self.current_color.name()
            button.setStyleSheet(
                f'background-color: {self.current_color.name()};')

    def critical_points(self, row, col) -> bool:
        one = (row * NUMBER_OF_COLUMN + col - NUMBER_OF_COLUMN - 1)
        two = (row * NUMBER_OF_COLUMN + col - NUMBER_OF_COLUMN + 1)
        three = (row * NUMBER_OF_COLUMN + col + NUMBER_OF_COLUMN - 1)
        four = (row * NUMBER_OF_COLUMN + col + NUMBER_OF_COLUMN + 1)

        if self.current_color.name() == '#808080':
            if row == col == 0:
                if self.buttons1[four][3] == '#808080':
                    return False
            elif row == col == NUMBER_OF_ROWS - 1:
                if self.buttons1[one][3] == '#808080':
                    return False
            elif row == 0 and col == NUMBER_OF_COLUMN - 1:
                if self.buttons1[three][3] == '#808080':
                    return False
            elif row == NUMBER_OF_ROWS - 1 and col == 0:
                if self.buttons1[two][3] == '#808080':
                    return False

            elif row == 0:
                if (self.buttons1[three][3] == '#808080'
                        or self.buttons1[four][3] == '#808080'):
                    return False
            elif row == NUMBER_OF_ROWS - 1:
                if (self.buttons1[one][3] == '#808080'
                        or self.buttons1[two][3] == '#808080'):
                    return False
            elif col == 0:
                if (self.buttons1[two][3] == '#808080'
                        or self.buttons1[four][3] == '#808080'):
                    return False
            elif col == NUMBER_OF_COLUMN - 1:
                if (self.buttons1[three][3] == '#808080'
                        or self.buttons1[one][3] == '#808080'):
                    return False

            else:
                if (self.buttons1[one][3] == '#808080' or
                        self.buttons1[two][3] == '#808080' or
                        self.buttons1[three][3] == '#808080' or
                        self.buttons1[four][3] == '#808080'):
                    return False

        return True

    # =========================================================================
    # задание цвета всем кнопкам. // из __init__
    def create_color_buttons(self, colors_layout):
        button = QPushButton(f'{BUTTON_NAME[0]}', self)
        button.clicked.connect(self.start_battle)
        colors_layout.addWidget(button)

        for idx, c in enumerate(BUTTON_COLORS):
            button = QPushButton(f'{BUTTON_NAME[idx + GLOBAL_STEP]}', self)
            button.clicked.connect(
                lambda _, color=c: self.change_current_color(color))
            colors_layout.addWidget(button)

    # изменить текущий цвет
    def change_current_color(self, color):
        self.current_color = color

    # начать битву
    def start_battle(self):
        ships: list[QPushButton(), int, int, str] = (
            list(filter(lambda x: x[3] == '#808080', self.buttons1)))

        rash = [x[1:3] for x in ships]
        all_ships: list = []
        one_ship: list = []
        i = 0
        while i != len(rash) or rash != []:
            one_ship.append(rash[i])
            el = rash[i]
            rash.remove(el)
            while True:
                if [el[0] + 1, el[1]] in rash:
                    el = [el[0] + 1, el[1]]
                    one_ship.append(el)
                    rash.remove(el)
                elif [el[0], el[1] + 1] in rash:
                    el = [el[0], el[1] + 1]
                    one_ship.append(el)
                    rash.remove(el)
                else:
                    all_ships.append(one_ship)
                    one_ship = []
                    break
        all_ships = [[*x[0], 'down' if len(x) >= 2 and x[0][0] + 1 == x[1][0]  else 'right', len(x)] for x in all_ships]
        pprint.pprint(all_ships)
        print()

    def __init__(self):
        super().__init__()

        self.setWindowTitle(NAME_WINDOW)
        self.setGeometry(INDENT_X, INDENT_Y, WIDTH_X, HEIGHT_Y)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # добавление поля обороны
        grid_layout1 = QGridLayout()
        main_layout.addLayout(grid_layout1)

        # добавление поля атаки
        grid_layout2 = QGridLayout()
        main_layout.addLayout(grid_layout2)

        # добавление кнопок
        colors_layout = QVBoxLayout()
        main_layout.addLayout(colors_layout)

        # создание осей координат
        self.create_rows(grid_layout1)
        self.create_cols(grid_layout1)
        self.create_rows(grid_layout2)
        self.create_cols(grid_layout2)

        self.buttons1: list = []
        self.buttons2: list = []
        self.colors = [QColor(BLUE_COLOR), QColor(GRAY_COLOR),
                       QColor(WHITE_COLOR), QColor(RED_COLOR)]
        self.current_color = self.colors[FLAG]

        # вывод на экран кнопок и полей
        self.create_grid(grid_layout1, grid_layout2)
        self.create_color_buttons(colors_layout)

        self._game = Game(NUMBER_OF_ROWS, NUMBER_OF_COLUMN)
        # потом 3-им аргументом будет кидаться сложность
        self._player = Player(NUMBER_OF_ROWS, NUMBER_OF_COLUMN)
