from ..dataclasses.cell_states import CellState
from ..dataclasses.point import Point
from ..core.algorithms import get_distance_manhattan, get_inner_points, is_in_range, get_second_point
from ..dataclasses.ship_definer import ShipDefiner
from ..exceptions.exceptions import ShipException
from ..interfaces.IPlayable import IPlayable
from random import Random
import random


class Game(IPlayable):
    def __init__(self, rows: int, columns: int, ship_definer: ShipDefiner):
        self.field = {}
        self.rows: int = rows
        self.columns: int = columns
        self.ship_definer = ship_definer
        self.ship_counter = {}

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self) -> int:
        return self.columns

    def set_ship(self, start_point: Point, end_point: Point) -> None or ShipException:
        Game.validate_cater_cornered(start_point, end_point)
        Game.validate_size_ship(start_point, end_point)
        self.check_count_ship(start_point, end_point)

        if not is_in_range(start_point.get_x(), 0, self.columns - 1, start_point.get_y(), 0, self.rows - 1):
            raise ShipException(f"Не принимаем cтартовые точки с отрицательными координатами {start_point}")

        if not is_in_range(end_point.get_x(), 0, self.columns - 1, end_point.get_y(), 0, self.rows - 1):
            raise ShipException(f"Не принимаем конечные точки с отрицательными координатами {start_point}")

        for p in get_inner_points(start_point, end_point):
            self.check_ship_near(p)

        size = get_distance_manhattan(start_point, end_point) + 1

        if self.ship_counter.get(size) is None:
            self.ship_counter[size] = 1
        else:
            self.ship_counter[size] += 1

        for p in get_inner_points(start_point, end_point):
            self.field[p] = CellState.SHIP_FOUND

    def pick_ship(self, point: Point) -> CellState:
        return CellState.SHIP_FOUND if self.field.get(point) else CellState.SHIP_NOTFOUND

    def check_ship_near(self, point: Point) -> None or ShipException:
        for p in point.get_points_around():
            x = p.get_x()
            y = p.get_y()

            if not is_in_range(x, 0, self.columns - 1, y, 0, self.rows - 1):
                continue

            if self.field.get(p) == CellState.SHIP_FOUND:
                raise ShipException(f"Рядом, на клетке {p} обнаружен корабль")

    @staticmethod
    def validate_cater_cornered(first: Point, second: Point) -> None or ShipException:
        if abs(first.get_x() - second.get_x()) > 0 and abs(first.get_y() - second.get_y()) > 0:
            raise ShipException(f"Нельзя ставить корабли наискось ({first}) и ({second})")

    @staticmethod
    def validate_size_ship(first: Point, second: Point) -> None or ShipException:
        size = get_distance_manhattan(first, second) + 1

        if size < 1 or size > 4:
            raise ShipException(f"Недопустимый размер корабля {size}")

    def check_count_ship(self, first: Point, second: Point) -> None or ShipException:
        size = get_distance_manhattan(first, second) + 1
        size_count_ship = self.ship_counter.get(size)

        if size == 1:
            if size_count_ship == self.ship_definer.count_one:
                raise ShipException(f"Нельзя добавить корабль первого типа, их уже {size_count_ship}")
        if size == 2:
            if size_count_ship == self.ship_definer.count_two:
                raise ShipException(f"Нельзя добавить корабль второго типа, их уже {size_count_ship}")
        if size == 3:
            if size_count_ship == self.ship_definer.count_three:
                raise ShipException(f"Нельзя добавить корабль третьего типа, их уже {size_count_ship}")
        if size == 4:
            if size_count_ship == self.ship_definer.count_four:
                raise ShipException(f"Нельзя добавить корабль четвертого типа, их уже {size_count_ship}")


def generate_field(rows: int, columns: int, ship_def: ShipDefiner) -> Game:
    game = Game(rows, columns, ship_def)
    seed = random.random()
    fill_field(game, seed, ship_def)
    return game


def fill_field(game: Game, seed: float, ship_def: ShipDefiner) -> None:
    random_gen = Random(seed)

    for size_ship in ship_def:
        while True:
            first = Point(random_gen.randint(0, game.columns - 1), random_gen.randint(0, game.rows - 1))
            second = get_second_point(first, size_ship)

            try:
                game.set_ship(first, second)
                break
            except ShipException:
                continue


def try_set_ship(first: Point, second: Point, game: Game):
    is_set: bool = False

    while not is_set:
        try:
            game.set_ship(first, second)
            is_set = True
        except ShipException:
            continue
