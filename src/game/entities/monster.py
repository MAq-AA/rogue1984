from __future__ import annotations

import logging
import math
import random
from dataclasses import dataclass
from enum import Enum

from game.entities.entity import Entity
from game.entities.move_logic import MoveDirection, PathFinder
from game.items.treasure import Treasure

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("debug.log", mode="w"))


class HostilityLevel(Enum):
    LOW = "2 cell radius to trigger"
    MEDIUM = "4 cell radius to trigger"
    HIGH = "6 cell radius to trigger"

    @property
    def int_value(self):
        return {
            HostilityLevel.LOW: 2,
            HostilityLevel.MEDIUM: 4,
            HostilityLevel.HIGH: 6,
        }[self]


class StatType(Enum):
    LOW = 0.5
    MEDIUM = 1
    HIGH = 1.5
    VERY_HIGH = 2.0


@dataclass
class Monster(Entity):
    depth: int = 0
    MIN_PART_OF_THE_STAT: float = 0.25
    hostility: HostilityLevel = HostilityLevel.LOW
    max_hp: int = 3
    str: int = 3
    dex: int = 3
    hp: int = 0
    name: __builtins__["str"] = "monster"
    is_triggered: bool = False

    @property
    def treasure(self):
        return Treasure(
            value=random.randint(
                1, self.hostility.int_value + self.max_hp + self.str + self.dex
            )
        )

    def get_move(self, level):
        if self.is_triggered:
            chasing_move = PathFinder.bfs(level, self, level.player)
            if chasing_move != MoveDirection.STAY.value:
                return chasing_move
        return self.get_random_move()

    def get_random_move(self):
        return random.choice(
            [
                MoveDirection.T.value,
                MoveDirection.R.value,
                MoveDirection.B.value,
                MoveDirection.L.value,
                MoveDirection.STAY.value,
            ]
        )

    def player_search(self, player_x_coord: int, player_y_coord: int):
        if not self.is_triggered:
            x_distance = math.fabs(self.x - player_x_coord) - 1
            y_distance = math.fabs(self.y - player_y_coord) - 1
            trigger_distance = self.hostility.int_value

            if x_distance <= trigger_distance and y_distance <= trigger_distance:
                self.is_triggered = True
