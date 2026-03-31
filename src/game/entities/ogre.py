import random
from dataclasses import dataclass

from api import Tile
from game.entities.character import Character
from game.entities.monster import Monster, HostilityLevel, StatType
from game.entities.move_logic import PathFinder, MoveDirection


@dataclass
class Ogre(Monster):
    tile: Tile = Tile.MONSTER_OGRE
    name = "ogre"
    preparing_to_attack = True

    def __post_init__(self):
        self.dex += int(self.depth * StatType.LOW.value)
        self.str += int(self.depth * StatType.VERY_HIGH.value)
        self.max_hp += int(self.depth * StatType.VERY_HIGH.value)
        self.hp = self.max_hp
        self.hostility = HostilityLevel.MEDIUM

    def attack(self, character: Character):
        if self.preparing_to_attack:
            self.preparing_to_attack = False
        else:
            is_got_hit = self.roll_dexterity() > character.roll_dexterity()

            if is_got_hit:
                character.get_damage(self.roll_strength())

            self.preparing_to_attack = True

    def get_move(self, level):
        if self.is_triggered:
            chasing_move = PathFinder.bfs(level, self, level.player)
            if chasing_move != MoveDirection.STAY.value:
                return chasing_move
        return self.get_random_move()

    def get_random_move(self):
        population = [
            MoveDirection.T.value,
            MoveDirection.R.value,
            MoveDirection.B.value,
            MoveDirection.L.value,
            MoveDirection.LT.value,
            MoveDirection.RT.value,
            MoveDirection.LB.value,
            MoveDirection.RB.value,
        ]
        return random.choices(
            population=population,
            weights=[12.5]*len(population),
            k=1
        )[0]