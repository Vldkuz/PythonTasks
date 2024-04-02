from algorithms import get_point_ships, get_move_by_complexity
from ..core.game import Game, generate_field
from ..dataclasses.level import Level
from ..dataclasses.point import Point
from ..interfaces.IPlayer import IPlayer


class ComputerPlayer(IPlayer):
    def __init__(self, enemy: Game, level: Level):
        self._enemy_field = enemy
        self._own_field = generate_field(enemy.rows, enemy.columns, enemy.ship_definer)
        self._made_steps = set()
        self._level = level

        # LEVEL.EASY = Вероятность подбить кораблик 25%
        # LEVEL.MEDIUM = Вероятность подбить кораблик 33%
        # LEVEL.HARD = Вероятность подбить кораблик 50%
        # LEVEL.UNREAL = Вероятность подбить кораблик 100%

    def get_next_move(self) -> Point:
        ship_site = get_point_ships(self._enemy_field.field.keys(), self._made_steps)
        return get_move_by_complexity(self._level, ship_site, self._made_steps)
