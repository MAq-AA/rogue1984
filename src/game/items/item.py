from dataclasses import dataclass

from api import DisplayItem
from game.base import GameObject


@dataclass
class Item(GameObject):
    hp: int = 0
    max_hp: int = 0
    dex: int = 0
    str_: int = 0
    value: int = 0
    name: str = "Generic item"

    def display_item(self):
        return DisplayItem(
            name=self.name,
            stat=max(self.hp, self.max_hp, self.dex, self.str_),
            id=id(self),
        )
