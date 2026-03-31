import random
from dataclasses import dataclass

from api import Tile
from game.entities.monster import HostilityLevel, Monster, StatType
from game.entities.move_logic import MoveDirection, PathFinder


@dataclass
class Ghost(Monster):
    tile: Tile = Tile.MONSTER_GHOST
    name = "ghost"
    _spawn_room = None
    _invisible = False

    def __post_init__(self):
        self.dex += int(self.depth * StatType.HIGH.value)
        self.str += int(self.depth * StatType.LOW.value)
        self.max_hp += int(self.depth * StatType.LOW.value)
        self.hp = self.max_hp
        self.hostility = HostilityLevel.LOW

    def get_move(self, level):
        if self.is_triggered:
            chasing_move = PathFinder.bfs(level, self, level.player)
            if chasing_move != MoveDirection.STAY.value:
                return chasing_move
        return self.teleport_within_room(level)

    def teleport_within_room(self, level):
        if self._spawn_room is not None:
            self.x = random.randint(self._spawn_room.x0 + 1, self._spawn_room.x1 - 1)
            self.y = random.randint(self._spawn_room.y0 + 1, self._spawn_room.y1 - 1)
        else:
            for room in level.rooms:
                if room.is_inside(self.x, self.y):
                    self._spawn_room = room
                    return self.teleport_within_room(level)
        return MoveDirection.STAY.value

    def flip_visibility(self):
        if self.is_triggered:
            self.tile = Tile.MONSTER_GHOST
        else:
            self.tile = random.choices(
                [Tile.MONSTER_GHOST, Tile.INVISIBLE_MONSTER_GHOST],
                weights=[10, 90],
                k=1,
            )[0]
