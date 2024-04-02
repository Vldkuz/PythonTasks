import unittest

from ..backend.dataclasses.cell_states import CellState
from ..backend.core.computer_player import ComputerPlayer
from ..backend.dataclasses.level import Level
from ..backend.core.game import Game
from ..backend.dataclasses.ship_definer import ShipDefiner
from ..backend.dataclasses.point import Point


class TestComputerPlayer(unittest.TestCase):
    _DEFAULT_ROWS = _DEFAULT_COLUMNS = 10
    _DEFAULT_SHIP_DEF = ShipDefiner(1, 2, 3, 4)

    def test_try_play_computer(self):
        game = Game(self._DEFAULT_ROWS, self._DEFAULT_COLUMNS, self._DEFAULT_SHIP_DEF)
        game.set_ship(Point(1, 2), Point(1, 4))
        computer = ComputerPlayer(game, Level.HARD)

        steps = []
        successd = []
        while len(successd) < 3:
            move = computer.get_next_move()
            steps.append(move)
            if game.pick_ship(move) == CellState.SHIP_FOUND:
                successd.append(move)

        self.assertLessEqual(len(steps), 6)


if __name__ == '__main__':
    unittest.main()
