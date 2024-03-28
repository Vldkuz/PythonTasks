# Здесь должна быть реализация второго игрока
from SeaBattle.src.exceptions.exceptions import ShipException
from SeaBattle.src.interfaces.IPlayer import IPlayer
from SeaBattle.src.backend.game import Game
from SeaBattle.src.backend.game_enums import *
import random

DEFAULT_ROWS = DEFAULT_COLUMNS = 10
EMPTY_DICT = 0
START_X = START_Y = 0
STEP = 1

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

START = 0
END = 4

X = 0
Y = 1

NEXT_PAIR = {
    UP: lambda x, y, modx, mody: (x % modx, (y + STEP) % mody),
    RIGHT: lambda x, y, modx, mody: ((x + STEP) % modx, y % mody),
    DOWN: lambda x, y, modx, mody: (x % modx, (y - STEP) % mody),
    LEFT: lambda x, y, modx, mody: ((x - STEP) % modx, y % mody)
}


class Player(IPlayer):
    def __init__(self, rows=DEFAULT_ROWS, columns=DEFAULT_COLUMNS, level=Level.EASY):
        self.rows = rows
        self.columns = columns
        self._IPlayable = Game(rows, columns)
        self._level = level
        self._enemy_field = {}

        self._SHIP_BY_DIRECTION = {
            Direction.UP: lambda ship_size: (
                random.randint(START_X, self.columns), random.randint(START_Y, self.rows - ship_size)),
            Direction.DOWN: lambda ship_size: (
                random.randint(START_X, self.columns), random.randint(START_Y + ship_size, self.rows)),
            Direction.LEFT: lambda ship_size: (
                random.randint(START_X + ship_size, self.columns), random.randint(START_Y, self.rows)),
            Direction.RIGHT: lambda ship_size: (
                random.randint(START_X, self.columns - ship_size), random.randint(START_Y, self.rows))
        }

        self._generate_ship_field()

    def set_feedback(self, coordinates: tuple[int, int], status: CellState) -> None:
        self._enemy_field[coordinates] = status

    def get_next_move(self) -> tuple[int, int]:
        # Пока реализация простая
        if len(self._enemy_field) == EMPTY_DICT:
            x = random.randint(START_X, self.columns)
            y = random.randint(START_Y, self.rows)
            return x, y

        for pair, state in self._enemy_field.items():
            if state == CellState.SHIP_FOUND:
                direction = random.randint(START, END)
                return NEXT_PAIR[direction](pair[X], pair[Y], self.rows, self.columns)

    def get_feedback(self, coordinates: tuple[int, int]) -> CellState:
        return self._IPlayable.pick_ship(coordinates)

    def _generate_ship_field(self):
        ships = {ShipSizes.BATTLE_SHIP, ShipSizes.CRUISER, ShipSizes.CRUISER,
                 ShipSizes.DESTROYER, ShipSizes.DESTROYER, ShipSizes.DESTROYER, ShipSizes.DESTROYER,
                 ShipSizes.BOAT, ShipSizes.BOAT, ShipSizes.BOAT, ShipSizes.BOAT, ShipSizes.BOAT}

        for ship in ships:
            self._generate_ship(ship)

    def _generate_ship(self, size_ship: ShipSizes):
        while True:
            direction = random.choice(list(Direction))
            coordinates_ship = self._SHIP_BY_DIRECTION.get(direction)(size_ship.value)
            try:
                self._IPlayable.set_ship(coordinates_ship, direction, size_ship)
                break
            except ShipException as e:
                continue
