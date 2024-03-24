from abc import ABC, abstractmethod

from SeaBattle.src.backend.game_enums import CellState


class IPlayer(ABC):

    @abstractmethod
    def get_next_move(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_feedback(self, coordinates: tuple[int, int], status: CellState) -> None:
        pass

    @abstractmethod
    def get_feedback(self, coordinates: tuple[int, int]) -> CellState:
        pass
