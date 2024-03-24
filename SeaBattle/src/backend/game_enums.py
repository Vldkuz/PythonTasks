import enum


class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Level(enum.Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    UNREAL = 3


class ShipSizes(enum.Enum):
    BATTLE_SHIP = 4
    CRUISER = 3
    DESTROYER = 2
    BOAT = 1


class CellState(enum.Enum):
    SHIP_FOUND = 0
    SHIP_NOTFOUND = 1


