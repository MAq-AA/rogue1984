import random
from dataclasses import dataclass

from api import Tile
from game.items.item import Item


@dataclass
class Scroll(Item):
    tile: Tile = Tile.ITEM_SCROLL

    @classmethod
    def get_random(cls, level):
        attr = random.choice(["max_hp", "dex", "str_"])
        value = random.randint(1, level)
        name = ""
        match attr:
            case "max_hp":
                name = "health"
            case "dex":
                name = "dexterity"
            case "str_":
                name = "strength"
            case "_":
                raise Exception(f"No such attribute: {attr}")
        name = f"Scroll of {name}"
        return cls(name=name, **{attr: value})  # type: ignore
