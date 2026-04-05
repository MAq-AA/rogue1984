from api import Tile
from game.base import GameObject
from game.entities import (
    Backpack,
    Character,
    Entity,
    Ghost,
    Mimic,
    Ogre,
    SnakeMage,
    Vampire,
    Zombie,
)
from game.game.fog_of_war import FogOfWar
from game.game.game import GameStatus
from game.game.level import Level
from game.items import Elixir, Food, Key, Scroll, Weapon
from game.rooms import Door, Room, Stair
from game.rooms.corridor import Corridor
from game.rooms.door import DoorColor

class_map = {
    "GameObject": GameObject,
    "Character": Character,
    "Entity": Entity,
    "Ghost": Ghost,
    "Mimic": Mimic,
    "Ogre": Ogre,
    "SnakeMage": SnakeMage,
    "Vampire": Vampire,
    "Zombie": Zombie,
    "Backpack": Backpack,
    "Elixir": Elixir,
    "Food": Food,
    "Key": Key,
    "Scroll": Scroll,
    "Weapon": Weapon,
    "Level": Level,
    "Room": Room,
    "Stair": Stair,
    "Corridor": Corridor,
    "Door": Door,
    "DoorColor": DoorColor,
    "GameStatus": GameStatus,
    "FogOfWar": FogOfWar,
}


class Writer:
    def to_dict(self, obj):
        data = dict(obj.__dict__)
        data["_type"] = obj.__class__.__name__
        match obj:
            case GameObject():
                data["tile"] = obj.tile.name
            case Character():
                data["tile"] = obj.tile.name
                data["backpack"] = self.to_dict(obj.backpack)
            case Backpack():
                data["items"] = [self.to_dict(item) for item in obj.items]
            case Level():
                data["items"] = [self.to_dict(item) for item in obj.items]
                data["monsters"] = [self.to_dict(monster) for monster in obj.monsters]
                data["players"] = self.to_dict(obj.player)
                data["rooms"] = [self.to_dict(room) for room in obj.rooms]
            case Room():
                pass
            case Stair():
                data["tile"] = obj.tile.name
            case Corridor():
                data["_door"] = self.to_dict(obj._door) if obj._door else None
                data["rooms"] = [self.to_dict(room) for room in obj.rooms]
            case Door():
                data["tile"] = obj.tile.name
                data["color"] = obj.color.value

        return data


class Reader:
    def from_dict(self, data):
        pass
