from dataclasses import dataclass, field
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
    DOOR_RED = auto()
    DOOR_BLUE = auto()
    DOOR_GREEN = auto()
    ITEM_WEAPON = auto()
    ITEM_ELIXIR = auto()
    ITEM_SCROLL = auto()
    ITEM_FOOD = auto()
    ITEM_KEY_RED = auto()
    ITEM_KEY_BLUE = auto()
    ITEM_KEY_GREEN = auto()
    UNKNOWN = auto()
    STAIR = auto()
    MONSTER_ZOMBIE = auto()
    MONSTER_VAMPIRE = auto()
    MONSTER_GHOST = auto()
    INVISIBLE_MONSTER_GHOST = auto()
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
    keys: str = ""


@dataclass(frozen=True)
class DisplayItem:
    name: str
    stat: int
    id: int


@dataclass(frozen=True)
class RunStats:
    treasure: int
    level: int
    enemies: int
    food: int
    elixirs: int
    scrolls: int
    attacks: int
    hits: int
    tiles: int


@dataclass(frozen=True)
class GameStats:
    runs: list[RunStats]
