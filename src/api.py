from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable


class Tile(Enum):
    EMPTY = auto()
    WALL_V = auto()
    WALL_H = auto()
    CORNER_TL = auto()
    CORNER_TR = auto()
    CORNER_BL = auto()
    CORNER_BR = auto()
    FLOOR = auto()
    CHARACTER = auto()
    CORRIDOR = auto()
    DOOR = auto()
    ITEM_WEAPON = auto()
    ITEM_ELIXIR = auto()
    ITEM_SCROLL = auto()
    ITEM_FOOD = auto()
    ITEM_KEY = auto()
    UNKNOWN = auto()
    STAIR = auto()
    MONSTER_ZOMBIE = auto()
    MONSTER_VAMPIRE = auto()
    MONSTER_GHOST = auto()
    MONSTER_OGRE = auto()
    MONSTER_SNAKE_MAGE = auto()


class InputEvent(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    QUIT = auto()
    USE_WEAPON = auto()
    USE_FOOD = auto()
    USE_ELIXIR = auto()
    USE_SCROLL = auto()


@dataclass(frozen=True)
class DrawTile:
    x: int
    y: int
    tile: Tile


@dataclass(frozen=True)
class Frame:
    tiles: Iterable[DrawTile]
    hp: int
    max_hp: int
    max_hp_mod: int
    str: int
    str_mod: int
    dex: int
    dex_mod: int
    treasure: int
    level: int
    message: str = ""
    weapon: str = ""


@dataclass(frozen=True)
class DisplayItem:
    name: str
    stat: int
    id: int
