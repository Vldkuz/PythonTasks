from SeaBattle.src.backend.game_enums import *
from SeaBattle.src.exceptions.exceptions import *
from SeaBattle.src.interfaces.IPlayable import IPlayable


STANDARD_STANDOFF_FOR_GEN_RANGE = 1

X = 0
Y = 1

COORDINATES_GENERATOR = {
    Direction.UP: lambda x, y, ship_size: (range(x, x + ship_size), range(y, y + STANDARD_STANDOFF_FOR_GEN_RANGE)),
    Direction.RIGHT: lambda x, y, ship_size: (range(x, x + STANDARD_STANDOFF_FOR_GEN_RANGE), range(y, y + ship_size)),
    Direction.DOWN: lambda x, y, ship_size: (range(x, x - ship_size), range(y, y + STANDARD_STANDOFF_FOR_GEN_RANGE)),
    Direction.LEFT: lambda x, y, ship_size: (range(x, x + STANDARD_STANDOFF_FOR_GEN_RANGE), range(y - ship_size, y))
}


class Game(IPlayable):
    def __init__(self, rows, columns):
        self._field = {}
        self._max_rows = rows
        self._max_columns = columns

    def set_ship(self, coordinates: tuple[int, int], direction: Direction, ship_size: ShipSizes) -> None or ShipException:
        self._validate_add_ship(coordinates, direction, ship_size)  # Проверяем, можем ли поставить корабль
        coordinates_sequence = self._generate_coordinates_ship(coordinates, direction, ship_size)  # Формируем последовательность клеток для корабля

        for x in coordinates_sequence[X]:
            for y in coordinates_sequence[Y]:
                self._field[(x, y)] = CellState.SHIP_FOUND

    def pick_ship(self, coordinates: tuple[int, int]) -> CellState:
        return CellState.SHIP_NOTFOUND if self._field.get(coordinates) is None else CellState.SHIP_FOUND

    @staticmethod
    def _generate_coordinates_ship(coordinates: tuple[int, int], direction: Direction, ship_size: ShipSizes) -> tuple[range, range] or list[range, range]:
        return COORDINATES_GENERATOR.get(direction)(coordinates[X], coordinates[Y], ship_size.value)

    def _validate_add_ship(self, coordinates: tuple[int, int], direction: Direction, ship_size: ShipSizes) -> None or ShipException:

        coordinates_func = COORDINATES_GENERATOR.get(direction)

        if coordinates_func is None:
            raise ShipException(f"Нет такого направления {direction}")

        if not isinstance(ship_size, ShipSizes):
            raise ShipException(f"Нет такого размера корабля {ship_size}")

        coordinates_seq = coordinates_func(coordinates[X], coordinates[Y], ship_size.value)

        for x in coordinates_seq[X]:
            for y in coordinates_seq[Y]:
                self._validate_coordinates_overhead((x, y))

    def _validate_coordinates_overhead(self, coordinates: tuple[int, int]) -> ShipException or None:

        if (coordinates[X] > self._max_columns
                or coordinates[Y] > self._max_rows
                or coordinates[X] < 0 or coordinates[Y] < 0):
            raise ShipException(f'Выход за границу сетки {coordinates}')

        if (coordinates[X] - 1) < 0:
            left_x = coordinates[X]
        else:
            left_x = coordinates[X] - 1

        if (coordinates[X] + 1) > self._max_columns:
            right_x = coordinates[X]
        else:
            right_x = coordinates[X] + 1

        if (coordinates[Y] + 1) > self._max_rows:
            up_y = coordinates[Y]
        else:
            up_y = coordinates[Y] + 1

        if (coordinates[Y] - 1) < 0:
            down_y = coordinates[Y]
        else:
            down_y = coordinates[Y] - 1

        if (self._field.get((left_x, coordinates[Y])) == CellState.SHIP_FOUND
                or self._field.get((right_x, coordinates[Y])) == CellState.SHIP_FOUND
                or self._field.get((coordinates[X], up_y)) == CellState.SHIP_FOUND
                or self._field.get((coordinates[X], down_y)) == CellState.SHIP_FOUND):
            raise ShipException(f'Рядом находится корабль: {coordinates}')
