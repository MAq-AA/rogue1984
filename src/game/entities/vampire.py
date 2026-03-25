from dataclasses import dataclass

from api import Tile
from game.entities.monster import Monster


@dataclass
class Vampire(Monster):
    tile: Tile = Tile.MONSTER_VAMPIRE
    name = "vampire"

    def __post_init__(self):
        self.dex = int(3 + self.depth)
        self.str = int((3 + self.depth) / 3)
        self.max_hp = int((3 + self.depth) / 5)
        self.hp = self.max_hp
        self.hostility = 8
