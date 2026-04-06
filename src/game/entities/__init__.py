from game.entities.character import Backpack, Character
from game.entities.entity import Entity
from game.entities.ghost import Ghost
from game.entities.mimic import Mimic
from game.entities.ogre import Ogre
from game.entities.snake_mage import SnakeMage
from game.entities.vampire import Vampire
from game.entities.zombie import Zombie

monster_types = [Zombie, Vampire, Ghost, Ogre, SnakeMage, Mimic]
__all__ = [
    "Zombie",
    "Vampire",
    "Ghost",
    "Ogre",
    "SnakeMage",
    "Mimic",
    "Entity",
    "Character",
    "Backpack",
]
