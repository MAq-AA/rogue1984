import logging
import random

from api import Tile
from game.base import GameObject
from game.entities import monster_types
from game.entities.character import Character
from game.entities.entity import Entity
from game.entities.monster import Monster
from game.items.elixir import Elixir
from game.items.food import Food
from game.items.item import Item
from game.items.scroll import Scroll
from game.items.treasure import Treasure
from game.items.weapon import Weapon
from game.rooms.corridor import Corridor
from game.rooms.room import Room
from game.rooms.stair import Stair

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("debug.log", mode="w"))


class Level:
    def __init__(self, depth: int, player: Character):
        self.player = player
        self.depth = depth
        self.exited = False
        self.rooms: list[Room] = [Room(i) for i in range(9)]
        self.corridors = self.generate_corridors()
        self.starting_room: int = random.randint(0, 8)
        x = (self.rooms[self.starting_room].x0 + self.rooms[self.starting_room].x1) // 2
        y = (self.rooms[self.starting_room].y0 + self.rooms[self.starting_room].y1) // 2
        self.place(player, x, y)
        self.items: list[Item] = self.place_items()
        self.monsters: list[Monster] = self.place_monsters()
        self.message = ""
        self.stair = self.place_stair()

    def place(self, obj: GameObject, x=None, y=None):
        obj.place(x, y)

    def move(self, obj: GameObject, dx=0, dy=0):
        target = self[obj.x + dx, obj.y + dy]

        if target in [Tile.FLOOR, Tile.CORRIDOR]:
            obj.move(dx, dy)
        if isinstance(target, Item) and obj is self.player:
            if self.player.backpack.put(target):
                self.remove(target)
            obj.move(dx, dy)
        if isinstance(target, Monster) and obj is self.player:
            self.fight(obj, target)
        if target == Tile.STAIR and obj is self.player:
            self.exited = True
            obj.move(dx, dy)

    def fight(self, attacker: Entity, defender: Entity):
        hit = random.randint(0, attacker.dex + attacker.dex_mod) > random.randint(
            0, defender.dex + defender.dex_mod
        )
        if hit:
            dmg = random.randint(
                0, attacker.str + attacker.str_mod + attacker.weapon.str_
            )
            defender.hp -= dmg
            self.message = f"{attacker.name} hit {defender.name} for {dmg} damage"
            if defender.hp <= 0:
                self.remove(defender)

    def end_turn(self):
        for monster in self.monsters:
            dx, dy = monster.get_move()
            self.move(monster, dx, dy)

    def remove(self, obj: GameObject):
        if isinstance(obj, Monster):
            self.monsters.remove(obj)
        if isinstance(obj, Item):
            self.items.remove(obj)

    def generate_corridors(self):
        adjacency = {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 5],
            3: [0, 4, 6],
            4: [1, 3, 5, 7],
            5: [2, 4, 8],
            6: [3, 7],
            7: [4, 6, 8],
            8: [5, 7],
        }
        corridors: list[Corridor] = []
        connected = [self.rooms[0]]
        while len(connected) < len(self.rooms):
            room1 = random.choice(connected)
            room2 = self.rooms[random.choice(adjacency[room1.id])]
            if room2 in connected:
                continue
            corridor = Corridor([room1, room2])
            corridors.append(corridor)
            connected.append(room2)
        return corridors

    def place_monsters(self) -> list[Monster]:
        monsters = []
        n_monsters = self.depth + 2
        to_place = random.choices(
            monster_types, k=n_monsters, weights=[0.5, 0.3, 0.2, 0.1, 0.1]
        )
        for monster_type in to_place:
            x, y = self._get_random_coords()
            monsters.append(monster_type(depth=self.depth, x=x, y=y))
        return monsters

    def place_items(self) -> list[Item]:
        new_items = []
        n_items = self.depth + 2
        to_place = random.choices(
            [
                Weapon,
                Elixir,
                Scroll,
                Food,
            ],
            k=n_items,
            weights=[0.1, 0.2, 0.2, 0.5],
        )
        for item_type in to_place:
            new_items.append(item_type.get_random(level=self.depth))
            x, y = self._get_random_coords()
            self.place(new_items[-1], x=x, y=y)
        return new_items

    def place_stair(self):
        stair = Stair()
        x, y = self._get_random_coords()
        self.place(stair, x=x, y=y)
        return stair

    def _get_random_coords(self):
        room_id = random.randint(0, 8)
        if room_id == self.starting_room:
            room_id = (room_id + 1) % 9
        room = self.rooms[room_id]
        x = random.randint(room.x0 + 1, room.x1 - 1)
        y = random.randint(room.y0 + 1, room.y1 - 1)
        return x, y

    def __getitem__(self, k) -> Tile | GameObject:
        x, y = k
        ret = Tile.EMPTY
        if (self.player.x, self.player.y) == (x, y):
            return self.player
        for item in self.items:
            if (item.x, item.y) == (x, y):
                return item
        for m in self.monsters:
            if (m.x, m.y) == (x, y):
                return m
        for room in self.rooms:
            if room.is_wall(x, y):
                ret = Tile.WALL_H
            if room.is_floor(x, y):
                ret = Tile.FLOOR
        for c in self.corridors:
            if c.is_inside(x, y):
                ret = Tile.CORRIDOR
        if (self.stair.x, self.stair.y) == (x, y):
            ret = Tile.STAIR
        return ret
