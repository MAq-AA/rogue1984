import json
import logging
from enum import Enum
from typing import cast

from api import Tile
from game.base import GameObject
from game.constants import SAVEFILE
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
from game.entities.monster import HostilityLevel, Monster
from game.game.fog_of_war import FogOfWar
from game.game.game import Game, GameStatus
from game.game.level import Level
from game.items import Elixir, Food, Key, Scroll, Weapon
from game.items.item import Item
from game.items.treasure import Treasure
from game.rooms import Door, Room, Stair
from game.rooms.corridor import Corridor
from game.rooms.door import DoorColor

class_map = {
    "Game": Game,
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
    "Tile": Tile,
    "HostilityLevel": HostilityLevel,
    "Treasure": Treasure,
}

logger = logging.getLogger(__name__)


class Writer:
    def to_dict(self, obj):
        data = dict(obj.__dict__)
        data["_type"] = obj.__class__.__name__
        if "tile" in data:
            data["tile"] = self.to_dict(data["tile"])
        match obj:
            case Character():
                data["backpack"] = self.to_dict(obj.backpack)
                data["weapon"] = self.to_dict(obj.weapon) if obj.weapon else None
            case Monster():
                data["weapon"] = self.to_dict(obj.weapon) if obj.weapon else None
                data["hostility"] = self.to_dict(obj.hostility)
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
                data["door_colors"] = [self.to_dict(color) for color in obj.door_colors]
                data["stair"] = self.to_dict(obj.stair)
            case Room():
                pass
            case Stair():
                pass
            case Corridor():
                data["_door"] = self.to_dict(obj._door) if obj._door else None
                data["rooms"] = [self.to_dict(room) for room in obj.rooms]
            case Door():
                data["color"] = self.to_dict(obj.color)
            case Key():
                data["color"] = self.to_dict(obj.color)
            case Game():
                data["level"] = self.to_dict(obj.level)
                data["game_status"] = self.to_dict(obj.game_status)
                data["fog_of_war"] = None
                data["ui"] = None
            case GameObject():
                pass
            case Enum():
                data = {"_type": data["_type"], "name": obj.name}

        return data

    def save_to_file(self, game: Game, filename: str = SAVEFILE):
        with open("dict.json", "w") as f:
            from pprint import pformat

            f.write(pformat(self.to_dict(game)))
        with open(filename, "w") as f:
            json.dump(self.to_dict(game), f, indent=2)


class Reader:
    def load_from_file(self, filename: str = SAVEFILE) -> Game:
        with open(filename, "r") as f:
            data = json.load(f)
        return cast(Game, self.from_dict(data))

    def transfer(self, data, obj):
        for attr in data:
            if attr != "_type":
                setattr(obj, attr, data[attr])
        return obj

    def from_dict(self, data):
        cls = class_map[data.pop("_type")]
        if "tile" in data:
            data["tile"] = self.from_dict(data["tile"])
        match cls:
            case cls if issubclass(cls, Game):
                level = cast(Level, self.from_dict(data["level"]))
                game_status = cast(GameStatus, self.from_dict(data["game_status"]))
                game = Game(ui=None)
                game.level = level
                game.game_status = game_status
                game.fog_of_war = FogOfWar(level)
                return game
            case cls if issubclass(cls, Level):
                data["items"] = cast(
                    list[Item], [self.from_dict(item) for item in data["items"]]
                )
                data["monsters"] = cast(
                    list[Monster],
                    [self.from_dict(monster) for monster in data["monsters"]],
                )
                data["player"] = cast(Character, self.from_dict(data["player"]))
                data["rooms"] = cast(
                    list[Room], [self.from_dict(room) for room in data["rooms"]]
                )
                data["corridors"] = [
                    self.from_dict(corridor) for corridor in data["corridors"]
                ]
                data["door_colors"] = [
                    self.from_dict(color) for color in data["door_colors"]
                ]
                data["stair"] = self.from_dict(data["stair"])
                level = Level(depth=data["depth"])
                self.transfer(data, level)
                return level
            case cls if issubclass(cls, Character):
                backpack = cast(Backpack, self.from_dict(data.pop("backpack")))
                weapon = cast(Weapon, self.from_dict(data.pop("weapon")))
                return Character(
                    x=data["x"],
                    y=data["y"],
                    hp=data["hp"],
                    max_hp=data["max_hp"],
                    max_hp_mod=data["max_hp_mod"],
                    str=data["str"],
                    str_mod=data["str_mod"],
                    dex=data["dex"],
                    dex_mod=data["dex_mod"],
                    backpack=backpack,
                    weapon=weapon,
                )
            case cls if issubclass(cls, Monster):
                data["weapon"] = cast(Weapon, self.from_dict(data.pop("weapon")))
                data["hostility"] = self.from_dict(data["hostility"])
                monster = cls()
                self.transfer(data, monster)
                return monster
            case cls if issubclass(cls, Backpack):
                items = [self.from_dict(item) for item in data["items"]]
                backpack = Backpack()
                backpack.items = items
                return backpack
            case cls if issubclass(cls, Room):
                room = Room(id=data["id"])
                self.transfer(data, room)
                return room
            case cls if issubclass(cls, Stair):
                return Stair(x=data["x"], y=data["y"], tile=data["tile"])
            case cls if issubclass(cls, Corridor):
                data["_door"] = self.from_dict(data["_door"]) if data["_door"] else None
                rooms = [self.from_dict(room) for room in data["rooms"]]
                corridor = Corridor(rooms=rooms)
                self.transfer(data, corridor)
                return corridor
            case cls if issubclass(cls, Door):
                door = Door(x=data["x"], y=data["y"], tile=data["tile"])
                self.transfer(data, door)
                door.color = self.from_dict(data["color"])
                return door
            case cls if issubclass(cls, Key):
                key = Key()
                self.transfer(data, key)
                key.color = self.from_dict(data["color"])
                return key
            case cls if issubclass(cls, GameObject):
                obj = cls(x=data["x"], y=data["y"], tile=data["tile"])
                self.transfer(data, obj)
                return obj
            case cls if issubclass(cls, Enum):
                return cls[data["name"]]
            case _:
                raise ValueError(f"Unknown data format: {data}")
