import logging
import random
from pprint import pformat

from api import Tile
from game.base import GameObject
from game.constants import MAX_DEPTH
from game.entities import Ghost, Ogre, monster_types
from game.entities.character import Character
from game.entities.entity import Entity
from game.entities.monster import Monster
from game.items.elixir import Elixir
from game.items.food import Food
from game.items.item import Item
from game.items.key import Key
from game.items.scroll import Scroll
from game.items.weapon import Weapon
from game.rooms.corridor import Corridor
from game.rooms.door import Door, DoorColor
from game.rooms.room import Room
from game.rooms.stair import Stair

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("debug.log", mode="w"))


class CollisionException(Exception):
    pass


class Level:
    def __init__(self, depth: int, player: Character):
        self.player = player
        self.depth = depth
        self.exited = False
        self.items: list[Item] = []
        self.monsters: list[Monster] = []
        self.rooms: list[Room] = [Room(i) for i in range(9)]
        self.corridors = self.generate_corridors()
        self.starting_room: int = random.randint(0, 8)
        self.door_colors: list[DoorColor] = []
        self.place_doors()
        self.place_keys()
        x = (self.rooms[self.starting_room].x0 + self.rooms[self.starting_room].x1) // 2
        y = (self.rooms[self.starting_room].y0 + self.rooms[self.starting_room].y1) // 2
        self.place(player, x, y)
        self.stair = Stair()
        self.place_stair()  # place stair before monsters and items to avoid placing them on top of it
        self.place_items()
        self.place_monsters()
        self.message = ""

    def place(self, obj: GameObject, x=None, y=None):
        obj.place(x, y)

    def move(self, obj: GameObject, dx=0, dy=0):
        target = self[obj.x + dx, obj.y + dy]

        if target in [Tile.FLOOR, Tile.CORRIDOR]:
            obj.move(dx, dy)
        elif isinstance(target, Item) and obj is self.player:
            if self.player.backpack.put(target):
                self.remove(target)
                self.message += f"You picked up {target.name}\n"
            obj.move(dx, dy)
        if isinstance(target, Door):
            if not target.closed:
                obj.move(dx, dy)
            elif isinstance(obj, Character):
                obj.open_door(target)
        elif isinstance(target, Character) and isinstance(obj, Monster):
            self.do_attack(obj, target)
        elif isinstance(target, Monster) and isinstance(obj, Character):
            self.do_attack(obj, target)
        elif target == Tile.STAIR and obj is self.player:
            self.exited = True
            obj.move(dx, dy)

    def do_attack(self, attacker: Entity, defender: Entity):
        defender_hp_before_attack = defender.hp
        attacker.attack(defender)
        dmg = defender_hp_before_attack - defender.hp
        if dmg > 0:
            self.message += f"{attacker.name} hit {defender.name} for {dmg} damage\n"
            if self.player.is_stunned:
                self.message += "you are stunned\n"
            if defender.hp <= 0:
                self.remove(defender)
                self.message += "... and killed it!\n"
                if isinstance(defender, Monster) and isinstance(attacker, Character):
                    attacker.backpack.put(defender.treasure)
        elif not isinstance(attacker, Ogre) or attacker.preparing_to_attack:
            self.message += f"{attacker.name} missed {defender.name}\n"

    def end_turn(self):
        for monster in self.monsters:
            monster.player_search(self.player.x, self.player.y)
            if isinstance(monster, Ghost):
                monster.flip_visibility()
            move = monster.get_move(self)
            first_target = self[monster.x + move[0], monster.y + move[1]]
            self.move(monster, move[0], move[1])
            if isinstance(monster, Ogre):
                move = monster.get_move(self)
                second_target = self[monster.x + move[0], monster.y + move[1]]
                if not (first_target is self.player and second_target is self.player):
                    if first_target != Tile.CORRIDOR:
                        self.move(monster, move[0], move[1])

    def remove(self, obj: GameObject):
        if isinstance(obj, Monster):
            self.monsters.remove(obj)
        if isinstance(obj, Item):
            self.items.remove(obj)

    def drop(self, item: Item):
        x, y = self.find_free_adjacent(self.player.x, self.player.y)
        if x != -1:
            self.items.append(item)
            self.place(item, x, y)

    def find_free_adjacent(self, x, y) -> tuple[int, int]:
        offsets = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        random.shuffle(offsets)
        for dx, dy in offsets:
            if self[x + dx, y + dy] in [Tile.FLOOR, Tile.CORRIDOR]:
                return x + dx, y + dy
        return -1, -1

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

    def place_doors(self):
        door_colors = [DoorColor.RED, DoorColor.GREEN, DoorColor.BLUE]
        n_doors = random.randint(0, 3)
        for c in door_colors[:n_doors]:
            random.choice(self.corridors).close(c)
            self.door_colors.append(c)

    def place_keys(self):
        for c in self.door_colors:
            self.items.append(Key.get(color=c))
            room_ids = self.accessible_rooms(c)
            key_room = self.rooms[random.choice(room_ids)]
            self.place(self.items[-1], *key_room.get_random_coords())

    def accessible_rooms(self, door_color: DoorColor) -> list[int]:
        room_ids = [self.starting_room]
        i = 0
        while i < len(room_ids):
            for corridor in self.corridors:
                if corridor.closed and corridor.closed.color == door_color:
                    continue
                if self.rooms[room_ids[i]] in corridor.rooms:
                    for room in corridor.rooms:
                        if room.id not in room_ids:
                            room_ids.append(room.id)
            i += 1
        return room_ids

    def place_monsters(self):
        n_monsters = self.depth + 2
        to_place = random.choices(
            monster_types, k=n_monsters, weights=[0.5, 0.3, 0.2, 0.1, 0.1]
        )
        for monster_type in to_place:
            try:
                x, y = self._get_random_coords()
                self.monsters.append(monster_type(depth=self.depth, x=x, y=y))
            except CollisionException:
                continue

    def place_items(self):
        n_items = MAX_DEPTH - self.depth
        to_place = random.choices(
            [
                Weapon,
                Elixir,
                Scroll,
                Food,
            ],
            k=n_items,
            weights=[0.15, 0.2, 0.15, 0.5],
        )
        for item_type in to_place:
            try:
                x, y = self._get_random_coords()
                self.items.append(item_type.get_random(level=self.depth))
                logger.debug(
                    f"generated coords: {x}, {y}. Current contents: {self[x, y]}"
                )
                self.place(self.items[-1], x=x, y=y)
            except CollisionException:
                continue

    def place_stair(self):
        retries = 100
        for i in range(retries):
            x, y = self._get_random_coords()
            if self._corridor_obstructed(x, y):
                continue
            else:
                break
        self.place(self.stair, x=x, y=y)

    def _get_random_coords(self) -> tuple[int, int]:
        for _ in range(3):
            room_id = random.randint(0, 8)
            if room_id == self.starting_room:
                room_id = (room_id + 1) % 9
            room = self.rooms[room_id]
            x, y = room.get_random_coords()
            if self[x, y] == Tile.FLOOR:
                return x, y
        raise CollisionException

    def _corridor_obstructed(self, x, y):
        return Tile.CORRIDOR in [
            self[x + 1, y],
            self[x - 1, y],
            self[x, y + 1],
            self[x, y - 1],
        ]

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
                if c.door(x, y):
                    ret = c.door(x, y)
        if (self.stair.x, self.stair.y) == (x, y):
            ret = Tile.STAIR
        return ret
