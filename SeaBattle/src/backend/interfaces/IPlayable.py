from abc import ABC, abstractmethod
from ..dataclasses.cell_states import CellState
from ..exceptions.exceptions import ShipException
from ..dataclasses.point import Point


class IPlayable(ABC):

    @abstractmethod
    def set_ship(self, start_point: Point, end_point: Point) -> None or ShipException:
        pass

    @abstractmethod
    def pick_ship(self, point: Point) -> CellState:
        pass
