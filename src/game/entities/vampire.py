import sys
from dataclasses import dataclass

from api import Tile
from game.entities.character import Character
from game.entities.entity import Entity
from game.entities.monster import HostilityLevel, Monster, StatType
from game.entities.move_logic import MoveDirection, PathFinder


@dataclass
class Vampire(Monster):
    tile: Tile = Tile.MONSTER_VAMPIRE
    name: str = "vampire"
    COUNT_LEVEL_FOR_RAISE_STEALS_HP: int = 10
    first_defence: bool = True

    def __post_init__(self):
        self.dex += int(self.depth * StatType.HIGH.value)
        self.str += int(self.depth * StatType.MEDIUM.value)
        self.max_hp += int(self.depth * StatType.HIGH.value)
        self.hp = self.max_hp
        self.hostility = HostilityLevel.HIGH

    def attack(self, other: Entity):
        is_got_hit = self.roll_dexterity(for_defence=False) > other.roll_dexterity()

        if is_got_hit:
            other.get_damage(self.roll_strength())
            other.max_hp -= 1 + int(self.depth / self.COUNT_LEVEL_FOR_RAISE_STEALS_HP)

    def roll_dexterity(self, for_defence: bool = True):
        if self.first_defence and for_defence:
            self.first_defence = False
            return sys.maxsize
        return super().roll_dexterity()

    def get_move(self, level):
        if self.is_triggered:
            chasing_move = PathFinder.bfs(level, self, level.player)
            if chasing_move != MoveDirection.STAY.value:
                return chasing_move
        return MoveDirection.STAY.value
