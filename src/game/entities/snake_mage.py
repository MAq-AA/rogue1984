import random
from dataclasses import dataclass

from api import Tile
from game.entities.entity import Entity
from game.entities.character import Character
from game.entities.monster import HostilityLevel, Monster, StatType
from game.entities.move_logic import MoveDirection, PathFinder


@dataclass
class SnakeMage(Monster):
    tile: Tile = Tile.MONSTER_SNAKE_MAGE
    name: __builtins__["str"] = "snake mage"
    _last_move: tuple | None = None
    CHANCE_TO_STUN: float = 0.1

    def __post_init__(self):
        self.dex += int(self.depth * StatType.VERY_HIGH.value)
        self.str += int(self.depth * StatType.LOW.value)
        self.max_hp += int(self.depth * StatType.LOW.value)
        self.hp = self.max_hp
        self.hostility = HostilityLevel.HIGH

    def attack(self, other: Entity):
        is_got_hit = self.roll_dexterity() > other.roll_dexterity()

        if is_got_hit:
            other.get_damage(self.roll_strength())
            if random.random() < self.CHANCE_TO_STUN:
                other.is_stunned = True

    def get_move(self, level):
        if self.is_triggered:
            chasing_move = PathFinder.bfs(level, self, level.player)
            if chasing_move != MoveDirection.STAY.value:
                return chasing_move
        return self.get_random_move()

    def get_random_move(self):
        population = [
            MoveDirection.LT.value,
            MoveDirection.RT.value,
            MoveDirection.RB.value,
            MoveDirection.LB.value,
        ]

        available_moves = [move for move in population if move != self._last_move]

        weights = [25] * len(available_moves)

        chosen = random.choices(population=available_moves, weights=weights, k=1)[0]

        self._last_move = chosen
        return chosen
