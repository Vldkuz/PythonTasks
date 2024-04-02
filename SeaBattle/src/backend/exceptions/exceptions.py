class ShipException(Exception):
    def __init__(self, error: str):
        super().__init__()
        self.__error = error

    def __str__(self) -> str:
        return self.__error

