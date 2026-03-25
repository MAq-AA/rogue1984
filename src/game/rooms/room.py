import random

from game import constants


class Room:
    def __init__(self, id: int):
        self.id = id
        self.discovered = False
        x = (id % 3) * (constants.LEVEL_WIDTH // 3)
        y = (id // 3) * (constants.LEVEL_HEIGHT // 3)
        self.x0 = random.randint(x + 1, x + constants.LEVEL_WIDTH // 3 - 7)
        self.y0 = random.randint(y + 1, y + constants.LEVEL_HEIGHT // 3 - 5)
        self.x1 = random.randint(self.x0 + 5, x + constants.LEVEL_WIDTH // 3 - 2)
        self.y1 = random.randint(self.y0 + 3, y + constants.LEVEL_HEIGHT // 3 - 2)

    def is_floor(self, x, y):
        return self.is_inside(x, y) and not self.is_wall(x, y)

    def is_wall(self, x, y):
        return self.is_inside(x, y) and (
            x in [self.x0, self.x1] or y in [self.y0, self.y1]
        )

    def is_inside(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1