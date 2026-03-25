import random

from . import distance_to_line, in_range
from .room import Room


class Corridor:
    def __init__(self, rooms):
        self.rooms: list[Room] = sorted(rooms, key=lambda x: x.id)
        if self.rooms[1].id - self.rooms[0].id == 1:
            self.horizontal = True
            self.x0 = self.rooms[0].x1
            self.x1 = self.rooms[1].x0
            self.y0 = random.randint(self.rooms[0].y0 + 1, self.rooms[0].y1 - 1)
            self.y1 = random.randint(self.rooms[1].y0 + 1, self.rooms[1].y1 - 1)
        else:
            self.horizontal = False
            self.y0 = self.rooms[0].y1
            self.y1 = self.rooms[1].y0
            self.x0 = random.randint(self.rooms[0].x0 + 1, self.rooms[0].x1 - 1)
            self.x1 = random.randint(self.rooms[1].x0 + 1, self.rooms[1].x1 - 1)

    def is_inside(self, x, y):
        if in_range(x, self.x0, self.x1) and in_range(y, self.y0, self.y1):
            if x == self.x0 and y == self.y0:
                return True
            if x == self.x1 and y == self.y1:
                return True

            if self.horizontal:
                if self.x0 < self.x1:
                    start_x = self.x0 + 1
                    start_y = self.y0
                    end_x = self.x1 - 1
                    end_y = self.y1
                else:
                    start_x = self.x1 + 1
                    start_y = self.y1
                    end_x = self.x0 - 1
                    end_y = self.y0
            else:
                if self.y0 < self.y1:
                    start_x = self.x0
                    start_y = self.y0 + 1
                    end_x = self.x1
                    end_y = self.y1 - 1
                else:
                    start_x = self.x1
                    start_y = self.y1 + 1
                    end_x = self.x0
                    end_y = self.y0 - 1

            dist = distance_to_line((start_x, start_y), (end_x, end_y), (x, y))
            if dist <= 0.71:
                return True
        return False
