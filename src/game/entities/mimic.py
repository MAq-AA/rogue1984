import random
from dataclasses import dataclass

from api import Tile
from game.entities.monster import HostilityLevel, Monster, StatType
from game.entities.move_logic import MoveDirection, PathFinder


@dataclass
class Mimic(Monster):
    tile: Tile = random.choices(
        population=[Tile.ITEM_FOOD,
                    Tile.ITEM_ELIXIR,
                    Tile.ITEM_SCROLL,
                    Tile.ITEM_WEAPON,
                    Tile.ITEM_KEY_RED,
                    Tile.ITEM_KEY_BLUE,
                    Tile.ITEM_KEY_GREEN],
        weights=[20, 20, 20, 10, 5, 5, 5],
        k=1
    )[0]
    name = "mimic"

    def __post_init__(self):
        self.dex += int(self.depth * StatType.HIGH.value)
        self.str += int(self.depth * StatType.LOW.value)
        self.max_hp += int(self.depth * StatType.HIGH.value)
        self.hp = self.max_hp
        self.hostility = HostilityLevel.LOW

    def get_move(self, level):
        if self.is_triggered:
            chasing_move = PathFinder.bfs(level, self, level.player)
            if chasing_move != MoveDirection.STAY.value:
                return chasing_move

        return MoveDirection.STAY.value

    def player_search(self, level):
        if not self.is_triggered:
            super().player_search(level)
        elif self.tile != Tile.MONSTER_MIMIC:
            self.tile = Tile.MONSTER_MIMIC
