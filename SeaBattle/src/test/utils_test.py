import unittest
from ..backend.dataclasses.point import Point


class TestUtils(unittest.TestCase):
    def test_get_points_around_zero(self):
        first: Point = Point(0, 0)
        ans_points = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(-1, 1), Point(0, 1), Point(1, 1), Point(-1, 0),
                      Point(1, 0)]
        for p in first.get_points_around():
            self.assertEqual(p in ans_points, True)

    def test_get_points_around_five(self):
        first: Point = Point(5, 4)
        ans_points = [Point(4, 3), Point(5, 3), Point(6, 3), Point(6, 5), Point(5, 5), Point(4, 5), Point(4, 4),
                      Point(6, 4)]
        for p in first.get_points_around():
            self.assertEqual(p in ans_points, True)
