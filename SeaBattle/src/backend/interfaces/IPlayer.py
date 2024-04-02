from abc import ABC, abstractmethod
from ..dataclasses.point import Point


class IPlayer(ABC):
    @abstractmethod
    def get_next_move(self) -> Point:
        pass
