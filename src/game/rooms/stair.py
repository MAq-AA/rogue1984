from dataclasses import dataclass

from api import Tile
from game.base import GameObject


@dataclass
class Stair(GameObject):
    tile: Tile = Tile.STAIR