import json
import logging
from enum import Enum

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
from game.entities.monster import Monster
from game.game.game import Game, GameStatus
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
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("debug.log", mode="w"))


class Writer:
    def to_dict(self, obj):
        logger.debug(f"Serializing object {obj} of type {obj.__class__.__name__}")
        data = dict(obj.__dict__)
        data["_type"] = obj.__class__.__name__
        match obj:
            case Character():
                data["tile"] = obj.tile.name
                data["backpack"] = self.to_dict(obj.backpack)
                data["weapon"] = self.to_dict(obj.weapon) if obj.weapon else None
            case Monster():
                data["tile"] = obj.tile.name
                data["weapon"] = self.to_dict(obj.weapon) if obj.weapon else None
                data["hostility"] = obj.hostility.name
            case Backpack():
                data["items"] = [self.to_dict(item) for item in obj.items]
            case Level():
                data["items"] = [self.to_dict(item) for item in obj.items]
                data["monsters"] = [self.to_dict(monster) for monster in obj.monsters]
                data["player"] = self.to_dict(obj.player)
                data["rooms"] = [self.to_dict(room) for room in obj.rooms]
                data["corridors"] = [
                    self.to_dict(corridor) for corridor in obj.corridors
                ]
                data["door_colors"] = [color.name for color in obj.door_colors]
                data["stair"] = self.to_dict(obj.stair)
            case Room():
                pass
            case Stair():
                data["tile"] = obj.tile.name
            case Corridor():
                data["_door"] = self.to_dict(obj._door) if obj._door else None
                data["rooms"] = [self.to_dict(room) for room in obj.rooms]
            case Door():
                data["tile"] = obj.tile.name
                data["color"] = obj.color.name
            case Key():
                data["tile"] = obj.tile.name
                data["color"] = obj.color.name
            case Game():
                data["level"] = self.to_dict(obj.level)
                data["game_status"] = obj.game_status.name
                data["fog_of_war"] = None
                data["ui"] = None
            case GameObject():
                data["tile"] = obj.tile.name
            case Enum():
                data = obj.name

        return data

    def save_to_file(self, game: Game, filename: str = "savegame.json"):
        with open("dict.json", "w") as f:
            from pprint import pformat

            f.write(pformat(self.to_dict(game)))
        with open(filename, "w") as f:
            json.dump(self.to_dict(game), f, indent=2)


class Reader:
    def load_from_file(self, filename: str = "savegame.json") -> Game:
        with open(filename, "r") as f:
            data = json.load(f)
        return self.from_dict(data)

    def from_dict(self, data):
        pass
