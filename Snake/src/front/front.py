import sys
from collections import deque

from PyQt6.QtWidgets import (QApplication, QMainWindow, QGraphicsScene,
                             QGraphicsView, QVBoxLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QBrush, QPen
import random

CELL_SIZE = 20
BOARD_SIZE = 20


class SnakeGame(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake Game")
        self.setGeometry(0, 0, BOARD_SIZE * CELL_SIZE,
                         BOARD_SIZE * CELL_SIZE)

        self.scene = QGraphicsScene()
        self.showMaximized()
        self.view = QGraphicsView(self.scene)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setCentralWidget(self.view)

        self.snake = deque()
        self.food = SnakeGame.generate_food()
        self.snake.appendleft((0, 0))
        self.direction = Qt.Key.Key_D

        self.timer = QTimer()
        self.timer.timeout.connect(self.main_cycle)
        self.timer.start(100)

    @staticmethod
    def generate_food():
        return (random.randint(0, BOARD_SIZE - 1),
                random.randint(0, BOARD_SIZE - 1))

    def main_cycle(self):
        new_head = self.move_snake()
        self.check_callision(new_head)
        self.refresh_scene()

    def check_callision(self, new_head):
        if new_head in self.snake:
            self.timer.stop()
            return

        self.snake.appendleft(new_head)
        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def refresh_scene(self):
        self.scene.addRect(0, 0, BOARD_SIZE * CELL_SIZE,
                           BOARD_SIZE * CELL_SIZE,
                           brush=QBrush(QColor(50, 50, 50)))
        self.draw_snake()
        self.draw_food()

    def move_snake(self):
        new_head = head = self.snake[0]
        match self.direction:
            case Qt.Key.Key_A:
                new_head = (head[0], (head[1] - 1) % BOARD_SIZE)
            case Qt.Key.Key_D:
                new_head = (head[0], (head[1] + 1) % BOARD_SIZE)
            case Qt.Key.Key_W:
                new_head = ((head[0] - 1) % BOARD_SIZE, head[1])
            case Qt.Key.Key_S:
                new_head = ((head[0] + 1) % BOARD_SIZE, head[1])

        return new_head

    def draw_snake(self):
        brush = QBrush(QColor(0, 255, 0))
        for segment in self.snake:
            y, x = segment
            self.scene.addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE,
                               CELL_SIZE, pen=QPen(QColor('transparent')),
                               brush=brush)

    def draw_food(self):
        brush = QBrush(QColor(255, 0, 0))
        y, x = self.food
        self.scene.addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE,
                           pen=QPen(QColor('transparent')), brush=brush)

    def keyPressEvent(self, event):
        match event.key():
            case Qt.Key.Key_A if self.direction != Qt.Key.Key_D:
                self.direction = Qt.Key.Key_A
            case  Qt.Key.Key_D if self.direction != Qt.Key.Key_A:
                self.direction = Qt.Key.Key_D
            case  Qt.Key.Key_W if self.direction != Qt.Key.Key_S:
                self.direction = Qt.Key.Key_W
            case  Qt.Key.Key_S if self.direction != Qt.Key.Key_W:
                self.direction = Qt.Key.Key_S

