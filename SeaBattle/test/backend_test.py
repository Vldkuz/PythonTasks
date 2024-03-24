import unittest

from SeaBattle.src.backend.game import *
from SeaBattle.src.backend.player import *


class TestBackend(unittest.TestCase):
    _MAX_SHIP_SIZE = 4
    _DEFAULT_TEST_MAGIC_NUM = -20

    def test_setUpInvalidDirection(self):
        game = Game(DEFAULT_ROWS, DEFAULT_COLUMNS)
        direction = self._DEFAULT_TEST_MAGIC_NUM

        for row in range(DEFAULT_COLUMNS):
            for column in range(DEFAULT_ROWS):
                for size in range(self._MAX_SHIP_SIZE):
                    with self.assertRaises(ShipException):
                        game.set_ship((row, column), direction, size)

    def test_setUpInvalidShipSize(self):
        game = Game(DEFAULT_ROWS, DEFAULT_COLUMNS)
        size = self._DEFAULT_TEST_MAGIC_NUM

        for row in range(DEFAULT_COLUMNS):
            for column in range(DEFAULT_ROWS):
                for direction in Direction:
                    with self.assertRaises(ShipException):
                        game.set_ship((row, column), direction, size)

    def test_setUpValid(self):
        game = Game(DEFAULT_ROWS, DEFAULT_COLUMNS)
        game.set_ship((0, 0), Direction.UP, ShipSizes.BATTLE_SHIP)

    def test_pickFound(self):
        game = Game(DEFAULT_ROWS, DEFAULT_COLUMNS)
        game.set_ship((0, 0), Direction.UP, ShipSizes.BATTLE_SHIP)
        self.assertEqual(game.pick_ship((0, 0)), CellState.SHIP_FOUND)

    def test_pickNonFound(self):
        game = Game(DEFAULT_ROWS, DEFAULT_COLUMNS)
        game.set_ship((2, 0), Direction.UP, ShipSizes.BOAT)
        self.assertEqual(game.pick_ship((1, 0)), CellState.SHIP_NOTFOUND)


if __name__ == '__main__':
    unittest.main()
