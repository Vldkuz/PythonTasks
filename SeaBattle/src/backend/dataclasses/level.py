import enum
import random

from ..dataclasses.point import Point


class Level(enum.Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    UNREAL = 3


GET_POINT_BY_LEVEL = {
    Level.EASY: lambda ship_site: random.choice([ship_site, Point(ship_site.get_x() + 1, ship_site.get_y() + 1),
                                                 Point(ship_site.get_x() - 1, ship_site.get_y() - 1),
                                                 Point(ship_site.get_x() - 1, ship_site.get_y() + 1)]),
    Level.MEDIUM: lambda ship_site: random.choice([ship_site, Point(ship_site.get_x() + 1, ship_site.get_y() + 1), Point(ship_site.get_x() - 1, ship_site.get_y() + 1)]),
    Level.HARD: lambda ship_site: random.choice([ship_site, Point(ship_site.get_x() - 1, ship_site.get_y() - 1)]),
    Level.UNREAL: lambda ship_site: ship_site
}
