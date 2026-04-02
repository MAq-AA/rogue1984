from collections import deque
from enum import Enum

from api import Tile
from game import constants
from game.rooms.door import Door


class MoveDirection(Enum):
    STAY = (0, 0)
    L = (-1, 0)
    LT = (-1, -1)
    T = (0, -1)
    RT = (1, -1)
    R = (1, 0)
    RB = (1, 1)
    B = (0, 1)
    LB = (-1, 1)


class PathFinder:
    directions = [
        MoveDirection.L.value,
        MoveDirection.T.value,
        MoveDirection.R.value,
        MoveDirection.B.value,
    ]

    @classmethod
    def passable(cls, obj):
        if obj in [Tile.FLOOR, Tile.CORRIDOR]:
            return True
        if isinstance(obj, Door) and not obj.closed:
            return True

    @classmethod
    def bfs(cls, level, monster, player):
        max_x = constants.LEVEL_WIDTH
        max_y = constants.LEVEL_HEIGHT
        start = (monster.x, monster.y)
        end = (player.x, player.y)

        queue = deque([start])
        visited = set([start])
        prev = {start: None}
        end_is_find = False

        while queue:
            x, y = queue.popleft()

            if end_is_find:
                break

            for dx, dy in cls.directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < max_x and 0 <= ny < max_y:
                    if (nx, ny) == end:
                        prev[(nx, ny)] = (x, y)
                        cur = end
                        while prev[cur] != start:
                            cur = prev[cur]
                        return cur[0] - start[0], cur[1] - start[1]

                    if not cls.passable(level[nx, ny]):
                        continue
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        prev[(nx, ny)] = (x, y)

        return MoveDirection.STAY.value
