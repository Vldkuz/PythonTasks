from PyQt6.QtGui import QColor, QMouseEvent
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, \
    QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from screeninfo import get_monitors
from SeaBattle.src.backend.player import Player
from SeaBattle.src.backend.game import Game

NUMBER_OF_COLUMN = 10
NUMBER_OF_ROWS = 10
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


class ColorChanger(QWidget):

    # создание оси столбцов
    @staticmethod
    def create_cols(grid_layout):
        for j in range(NUMBER_OF_COLUMN):
            label = QLabel(str(j + GLOBAL_STEP))
            grid_layout.addWidget(label, j + GLOBAL_STEP, FLAG)

    # создание оси строк
    @staticmethod
    def create_rows(grid_layout):
        for i in range(NUMBER_OF_ROWS):
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
    def create_button(grid_layout, i, j, change_color, buttons, number):
        button = QPushButton()
        button.setMaximumSize(WIDTH_BUTTON_X, WIDTH_BUTTON_Y)
        button.setStyleSheet('background-color: blue;')

        button.clicked.connect(lambda _, row=i, col=j, grid_num=number:
                               change_color(row, col, grid_num))
        grid_layout.addWidget(button, i + GLOBAL_STEP, j + GLOBAL_STEP)
        buttons.append(button)

    def change_color(self, row, col, grid_num):
        if grid_num == FIELD_1:
            button = self.buttons1[row * NUMBER_OF_ROWS + col]
        else:
            button = self.buttons2[row * NUMBER_OF_COLUMN + col]
        button.setStyleSheet(
            f'background-color: {self.current_color.name()};')

    # =========================================================================
    # задание цвета всем кнопкам. // из __init__
    def create_color_buttons(self, colors_layout):
        for idx, c in enumerate(self.colors):
            btn = QPushButton(f'Color {idx + GLOBAL_STEP}', self)
            btn.clicked.connect(
                lambda _, color=c: self.change_current_color(color))
            colors_layout.addWidget(btn)

    # изменить текущий цвет
    def change_current_color(self, color):
        self.current_color = color

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

        self.buttons1 = []
        self.buttons2 = []
        self.colors = [QColor(RED_COLOR), QColor(BLUE_COLOR),
                       QColor(WHITE_COLOR), QColor(GRAY_COLOR)]
        self.current_color = self.colors[FLAG]

        # вывод на экран кнопок и полей
        self.create_grid(grid_layout1, grid_layout2)
        self.create_color_buttons(colors_layout)
