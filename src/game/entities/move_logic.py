import math
from collections import deque
from enum import Enum

from api import Tile
from game import constants


class PathFinder:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    PASSABLE = [Tile.FLOOR, Tile.CORRIDOR, Tile.INVISIBLE_FLOOR]

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

                    if level[nx, ny] not in cls.PASSABLE:
                        continue
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        prev[(nx, ny)] = (x, y)

        return 0, 0