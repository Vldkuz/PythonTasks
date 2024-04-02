from ..dataclasses.ship_sizes import ShipSizes


class ShipDefiner:
    def __init__(self, count_four: int, count_three: int, count_two: int, count_one: int):
        self.count_four = count_four
        self.count_three = count_three
        self.count_two = count_two
        self.count_one = count_one

    def __iter__(self):
        count_four = 0
        count_three = 0
        count_two = 0
        count_one = 0

        while count_four < self.count_four:
            yield ShipSizes.BATTLE_SHIP.value
            count_four += 1

        while count_three < self.count_three:
            yield ShipSizes.CRUISER.value
            count_three += 1

        while count_two < self.count_two:
            yield ShipSizes.DESTROYER.value
            count_two += 1

        while count_one < self.count_one:
            yield ShipSizes.BOAT.value
            count_one += 1
