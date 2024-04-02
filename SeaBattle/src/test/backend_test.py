import unittest

from ..backend.dataclasses.point import Point
from ..backend.exceptions.exceptions import ShipException
from ..backend.core.game import Game
from ..backend.dataclasses.ship_definer import ShipDefiner


class TestBackend(unittest.TestCase):
    _MAX_SHIP_SIZE = 4
    _DEFAULT_TEST_MAGIC_NUM = -20
    _DEFAULT_ROWS = 10
    _DEFAULT_COLS = 10
    _SHIP_DEF = ShipDefiner(1, 2, 3, 4)

    def test_cater_cornered(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        first: Point = Point(0, 0)
        second: Point = Point(1, 1)
        with self.assertRaises(ShipException):
            game.set_ship(first, second)

    def test_invalid_size_ship(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        points: list[Point] = [Point(5, 0), Point(6, 0), Point(0, 5), Point(0, 6)]
        first: Point = Point(0, 0)
        for point in points:
            with self.assertRaises(ShipException):
                game.set_ship(first, point)

    def test_invalid_pick_ship(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(0, 0), Point(0, 2))
        with self.assertRaises(ShipException):
            game.set_ship(Point(-10, -10), Point(-10, -12))

    def test_valid_pick_ship(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(0, 0), Point(0, 2))
        game.set_ship(Point(2, 0), Point(4, 0))

    def test_again_ship(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(0, 0), Point(0, 2))
        with self.assertRaises(ShipException):
            game.set_ship(Point(0, 0), Point(0, 2))

    def test_count_ships_four(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        with self.assertRaises(ShipException):
            game.set_ship(Point(0, 0), Point(0, 3))
            game.set_ship(Point(0, 9), Point(3, 9))

    def test_count_ship_three(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        with self.assertRaises(ShipException):
            game.set_ship(Point(0, 0), Point(0, 2))
            game.set_ship(Point(0, 9), Point(2, 9))
            game.set_ship(Point(5, 5), Point(7, 5))

    def test_valid_pick_ship(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLS, self._SHIP_DEF)
        game.set_ship(Point(1, 1), Point(1, 4))
        game.set_ship(Point(1, 9), Point(2, 9))
        game.set_ship(Point(3, 2), Point(3, 2))
        game.set_ship(Point(4, 4), Point(6, 4))
        game.set_ship(Point(4, 6), Point(6, 6))
        game.set_ship(Point(6, 8), Point(6, 9))
        game.set_ship(Point(9, 9), Point(9, 9))
        game.set_ship(Point(9, 1), Point(9, 2))
        game.set_ship(Point(9, 6), Point(9, 6))


if __name__ == '__main__':
    unittest.main()
