import unittest
from ..backend.core.algorithms import get_distance_manhattan, is_in_range, get_inner_points, get_second_point, \
    get_instep_point_ships, get_move_by_complexity
from ..backend.core.game import Game
from ..backend.dataclasses.cell_states import CellState
from ..backend.dataclasses.point import Point
from ..backend.dataclasses.ship_definer import ShipDefiner
from ..backend.dataclasses.level import Level


class TestAlgorithms(unittest.TestCase):
    _SHIP_DEF = ShipDefiner(1, 2, 3, 4)
    _DEFAULT_ROWS = 10
    _DEFAULT_COLS = 10
    _Level = Level.EASY

    def test_is_in_range(self):
        self.assertEqual(is_in_range(0, 0, 10, 1, 0, 20), True)
        self.assertEqual(is_in_range(5, 0, 10, 20, 0, 30), True)
        self.assertEqual(is_in_range(11, 0, 10, 10, 0, 10), False)
        self.assertEqual(is_in_range(10, 0, 10, 20, 0, 19), False)

    def test_get_distance_manhattan(self):
        first: Point = Point(0, 0)

        for i in range(0, 10):
            self.assertEqual(get_distance_manhattan(first, Point(0, i)), i)
        for j in range(0, 10):
            self.assertEqual(get_distance_manhattan(first, Point(j, 0)), j)

        for i in range(0, 10):
            for j in range(0, 10):
                self.assertEqual(get_distance_manhattan(first, Point(i, j)), i + j)

    def test_get_inner_points(self):
        first: Point = Point(5, 6)
        second: Point = Point(5, 10)
        third: Point = Point(9, 10)

        fs_ans = [Point(5, 6), Point(5, 7), Point(5, 8), Point(5, 9), Point(5, 10)]
        st_ans = [Point(5, 10), Point(6, 10), Point(7, 10), Point(8, 10), Point(9, 10)]

        fs = list(get_inner_points(first, second))
        st = list(get_inner_points(second, third))

        self.assertEqual(fs, fs_ans)
        self.assertEqual(st, st_ans)

    def test_get_point_ships(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(1, 1), Point(1, 2))
        point: Point = get_instep_point_ships(list(game.field.keys()), set())
        self.assertEqual(game.pick_ship(point), CellState.SHIP_FOUND)

    def test_get_second_point(self):
        size_ship: int = 4
        first: Point = Point(0, 0)
        second: Point = get_second_point(first, size_ship)
        self.assertEqual(get_distance_manhattan(first, second), size_ship - 1)

    def test_get_move_by_complexity_easy(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(1, 1), Point(1, 2))

        level: Level = Level.EASY

        point: Point = get_instep_point_ships(list(game.field.keys()), set())
        made_steps = set()
        is_found: bool = False

        for i in range(0, 4):
            move = get_move_by_complexity(level, point, made_steps)

            if game.pick_ship(move) == CellState.SHIP_FOUND:
                is_found = True

        self.assertEqual(is_found, True)

    def test_get_move_by_complexity_medium(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(1, 2), Point(1, 4))

        level: Level = Level.MEDIUM

        point: Point = get_instep_point_ships(list(game.field.keys()), set())
        made_steps = set()
        is_found: bool = False

        for i in range(0, 3):
            move = get_move_by_complexity(level, point, made_steps)

            if game.pick_ship(move) == CellState.SHIP_FOUND:
                is_found = True

        self.assertEqual(is_found, True)

    def test_get_move_by_complexity_hard(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(2, 3), Point(2, 4))

        level: Level = Level.HARD

        point: Point = get_instep_point_ships(list(game.field.keys()), set())
        made_steps = set()
        is_found: bool = False

        for i in range(0, 2):
            move = get_move_by_complexity(level, point, made_steps)

            if game.pick_ship(move) == CellState.SHIP_FOUND:
                is_found = True

        self.assertEqual(is_found, True)

    def test_get_move_by_complexity_unreal(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(2, 4), Point(2, 7))

        level: Level = Level.UNREAL

        point: Point = get_instep_point_ships(list(game.field.keys()), set())
        made_steps = set()
        move = get_move_by_complexity(level, point, made_steps)

        self.assertEqual(game.pick_ship(move), CellState.SHIP_FOUND)
