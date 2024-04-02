import enum

from ..dataclasses.point import Point


class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


GENERATOR_NEXT_POINT = {
    Direction.UP: lambda first, size_ship: Point(first.get_x(), first.get_y() + size_ship),
    Direction.DOWN: lambda first, size_ship: Point(first.get_x(), first.get_y() - size_ship),
    Direction.LEFT: lambda first, size_ship: Point(first.get_x() - size_ship, first.get_y()),
    Direction.RIGHT: lambda first, size_ship: Point(first.get_x() + size_ship, first.get_y())
}
