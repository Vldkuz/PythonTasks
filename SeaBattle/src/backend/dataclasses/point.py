class Point:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def __str__(self) -> str:
        return f'{self._x},{self._y}'

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_points_around(self):
        x = self._x - 1

        while x <= self._x + 1:
            yield Point(x, self._y - 1)
            x += 1

        while x >= self._x - 1:
            yield Point(x, self._y + 1)
            x -= 1

        yield Point(self._x - 1, self._y)
        yield Point(self._x + 1, self._y)

    def __gt__(self, other) -> bool:
        if other.get_x() == self._x:
            return self._y > other.get_y()
        else:
            return self._x > other.get_x()

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    def __eq__(self, other) -> bool:
        return self._x == other.get_x() and self._y == other.get_y()

