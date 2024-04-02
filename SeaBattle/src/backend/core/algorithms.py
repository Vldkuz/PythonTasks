# Здесь будут реализации полезных алгоритмов для работы программы
import random
from typing import Iterable
from ..dataclasses.direction import Direction, GENERATOR_NEXT_POINT
from ..dataclasses.level import Level, GET_POINT_BY_LEVEL
from ..dataclasses.point import Point


def is_in_range(x: int, x_less: int, x_more: int, y: int, y_less: int, y_more: int) -> bool:
    return (x_more >= x >= x_less) and (y_more >= y >= y_less)


def get_distance_manhattan(first: Point, second: Point) -> int:
    return abs(first.get_x() - second.get_x()) + abs(first.get_y() - second.get_y())
    # Вычисляется по Манхетеновской метрике, поскольку она совпадает с Евклидовой при расположении по вертикали или горизонтали


def get_inner_points(first: Point, second: Point) -> Iterable[Point]:
    start_x = min(first.get_x(), second.get_x())
    start_y = min(first.get_y(), second.get_y())
    end_y = max(first.get_y(), second.get_y())
    end_x = max(first.get_x(), second.get_x())

    if start_x == end_x:
        while start_y <= end_y:
            yield Point(start_x, start_y)
            start_y += 1
    else:
        while start_x <= end_x:
            yield Point(start_x, start_y)
            start_x += 1


def get_instep_point_ships(enemy_field: list, made_steps: set) -> Point:
    for step in enemy_field:
        if step in made_steps:
            continue
        return step


def get_move_by_complexity(level: Level, ship_site: Point, made_steps: set) -> Point:
    picked_move = GET_POINT_BY_LEVEL[level](ship_site)

    while picked_move in made_steps:
        picked_move = GET_POINT_BY_LEVEL[level](ship_site)

    made_steps.add(picked_move)
    return picked_move


def get_second_point(first: Point, size_ship: int):
    direction = random.choice(list(Direction))
    return GENERATOR_NEXT_POINT[direction](first, size_ship - 1)
