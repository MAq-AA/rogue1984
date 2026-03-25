from api import Tile
from game.base import GameObject
from game.items import fist


class Entity(GameObject):
    tile: Tile
    max_hp: int
    max_hp_mod = 0
    hp: int
    str: int
    str_mod = 0
    dex: int
    dex_mod = 0
    weapon = fist
    name: str = "unknown"
