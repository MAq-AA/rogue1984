from dataclasses import dataclass

from api import Tile
from game.entities.monster import Monster


@dataclass
class Ogre(Monster):
    tile: Tile = Tile.MONSTER_OGRE
    name = "ogre"

    def __post_init__(self):
        self.dex = int((3 + self.depth) / 5)
        self.str = int((3 + self.depth) * 1.5)
        self.max_hp = int((3 + self.depth) * 1.5)
        self.hp = self.max_hp
        self.hostility = 5
