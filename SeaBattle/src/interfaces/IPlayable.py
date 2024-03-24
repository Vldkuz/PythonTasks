from abc import ABC, abstractmethod
from SeaBattle.src.backend.game_enums import *
from SeaBattle.src.exceptions.exceptions import ShipException


class IPlayable(ABC):

    @abstractmethod
    def set_ship(self, coordinates: tuple[int, int], direction: Direction, ship_size: ShipSizes) -> None or ShipException:
        pass

    @abstractmethod
    def pick_ship(self, coordinates: tuple[int, int]) -> CellState:
        pass
