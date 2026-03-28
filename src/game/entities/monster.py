import logging
import random
from dataclasses import dataclass
from enum import Enum, auto
import math

from game.entities.move_logic import PathFinder
from game.entities.entity import Entity

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("debug.log", mode="w"))

class HostilityLevel(Enum):
    LOW = "2 cell radius to trigger"
    MEDIUM = "4 cell radius to trigger"
    HIGH = "6 cell radius to trigger"

    @property
    def value(self):
        return {
            HostilityLevel.LOW: 2,
            HostilityLevel.MEDIUM: 4,
            HostilityLevel.HIGH: 6
        }[self]

@dataclass
class Monster(Entity):
    depth: int = 0
    hostility: HostilityLevel = HostilityLevel.LOW
    max_hp: int = 0
    str: int = 0
    dex: int = 0
    hp: int = 0
    name = "monster"
    is_triggered = False
    last_move = None

    @property
    def treasure(self):
        return random.randint(1, self.hostility.value + self.max_hp + self.str + self.dex)

    def get_move(self, level):
        if self.is_triggered:
            return PathFinder.bfs(level, self, level.player)
        else:
            return random.choice(
                        [
                            [0, 1],
                            [0, -1],
                            [1, 0],
                            [-1, 0],
                        ]
                    )

    def player_search(self, player_x_coord: int, player_y_coord: int):
        x_distance = math.fabs(self.x - player_x_coord) - 1
        y_distance = math.fabs(self.y - player_y_coord) - 1
        trigger_distance = self.hostility.value

        if x_distance <= trigger_distance and y_distance <= trigger_distance:
            self.is_triggered = True
