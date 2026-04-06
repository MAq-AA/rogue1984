import random
from dataclasses import dataclass

from api import Tile
from game.entities.monster import HostilityLevel, Monster, StatType
from game.entities.move_logic import MoveDirection, PathFinder


@dataclass
class Zombie(Monster):
    tile: Tile = Tile.MONSTER_ZOMBIE
    name: str = "zombie"

    def __post_init__(self):
        self.dex += int(self.depth * StatType.LOW.value)
        self.str += int(self.depth * StatType.MEDIUM.value)
        self.max_hp += int(self.depth * StatType.HIGH.value)
        self.hp = self.max_hp
        self.hostility = HostilityLevel.MEDIUM

    def get_move(self, level):
        if self.is_triggered:
            chasing_move = PathFinder.bfs(level, self, level.player)
            if chasing_move != MoveDirection.STAY.value:
                return chasing_move

        return self.get_random_move()

    def get_random_move(self):
        return random.choices(
            population=[
                MoveDirection.T.value,
                MoveDirection.R.value,
                MoveDirection.B.value,
                MoveDirection.L.value,
                MoveDirection.LT.value,
                MoveDirection.RT.value,
                MoveDirection.LB.value,
                MoveDirection.RB.value,
                MoveDirection.STAY.value,
            ],
            weights=[5, 5, 5, 5, 5, 5, 5, 5, 60],
            k=1,
        )[0]
