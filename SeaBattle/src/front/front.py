from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QHBoxLayout
from screeninfo import get_monitors

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


class ColorChanger(QWidget):

    @staticmethod
    def create_cols(grid_layout):

        for j in range(NUMBER_OF_COLUMN):
            label = QLabel(str(j + GLOBAL_STEP))
            grid_layout.addWidget(label, j + GLOBAL_STEP, FLAG)

    @staticmethod
    def create_rows(grid_layout):
        for i in range(NUMBER_OF_ROWS):
            label = QLabel(chr(ASCII_START + i))
            grid_layout.addWidget(label, FLAG, i + GLOBAL_STEP)

    @staticmethod
    def create_button(grid_layout, i, j, change_color, buttons, number):
        button = QPushButton()
        button.setMaximumSize(WIDTH_BUTTON_X, WIDTH_BUTTON_Y)
        button.setStyleSheet('background-color: white;')
        button.clicked.connect(lambda _, row=i, col=j, grid_num=number:
                               change_color(row, col, grid_num))
        grid_layout.addWidget(button, i + GLOBAL_STEP, j + GLOBAL_STEP)
        buttons.append(button)

    def create_grid(self, grid_layout1, grid_layout2):
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLUMN):
                self.create_button(grid_layout1, i, j, self.change_color,
                                   self.buttons1, FIELD_1)
                self.create_button(grid_layout2, i, j, self.change_color,
                                   self.buttons2, FIELD_2)

    def create_color_buttons(self, colors_layout):
        for idx, c in enumerate(self.colors):
            btn = QPushButton(f'Color {idx + GLOBAL_STEP}', self)
            btn.clicked.connect(
                lambda _, color=c: self.change_current_color(color))
            colors_layout.addWidget(btn)

    def __init__(self):
        super().__init__()

        self.setWindowTitle(NAME_WINDOW)
        self.setGeometry(INDENT_X, INDENT_Y, WIDTH_X, HEIGHT_Y)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        grid_layout1 = QGridLayout()
        main_layout.addLayout(grid_layout1)

        grid_layout2 = QGridLayout()
        main_layout.addLayout(grid_layout2)

        colors_layout = QVBoxLayout()
        main_layout.addLayout(colors_layout)

        self.create_rows(grid_layout1)
        self.create_cols(grid_layout1)
        self.create_rows(grid_layout2)
        self.create_cols(grid_layout2)

        # Добавляем кнопки выбора цвета
        self.buttons1 = []
        self.buttons2 = []
        self.colors = [QColor('red'), QColor('green'), QColor('blue')]
        self.current_color = self.colors[FLAG]

        self.create_grid(grid_layout1, grid_layout2)
        self.create_color_buttons(colors_layout)

    def change_color(self, row, col, grid_num):
        if grid_num == FIELD_1:
            button = self.buttons1[row * NUMBER_OF_ROWS + col]
        else:
            button = self.buttons2[row * NUMBER_OF_COLUMN + col]
        button.setStyleSheet(f'background-color: {self.current_color.name()};')

    def change_current_color(self, color):
        self.current_color = color
