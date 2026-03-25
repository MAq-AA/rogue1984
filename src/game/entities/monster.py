import random
from dataclasses import dataclass

from game.entities.entity import Entity


@dataclass
class Monster(Entity):
    depth: int = 0
    hostility: int = 0
    max_hp: int = 0
    str: int = 0
    dex: int = 0
    hp: int = 0
    name = "monster"

    @property
    def treasure(self):
        return random.randint(1, self.hostility + self.max_hp + self.str + self.dex)

    def get_move(self):
        return random.choice(
            [
                [0, 1],
                [0, -1],
                [1, 0],
                [-1, 0],
            ]
        )
