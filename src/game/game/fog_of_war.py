import math
from _collections_abc import dict_values

from api import Tile
from game.base import GameObject
from game.constants import LEVEL_HEIGHT, LEVEL_WIDTH
from game.game.level import Level


class FogOfWar:
    def __init__(self, level: Level):
        self.all_fog_objects: dict[tuple[int, int], GameObject] = {}
        self.viewing_angle_coords: set[tuple[int, int]] = set()
        self.rooms_floor_coords: dict[int, set[tuple[int, int]]] = {}
        self.level = level
        for x in range(LEVEL_WIDTH):
            for y in range(LEVEL_HEIGHT):
                for room in self.level.rooms:
                    if room.is_inside(x, y):
                        self.all_fog_objects[(x, y)] = GameObject(
                            x=x, y=y, tile=Tile.EMPTY
                        )
                for corridor in self.level.corridors:
                    if corridor.is_inside(x, y):
                        self.all_fog_objects[(x, y)] = GameObject(
                            x=x, y=y, tile=Tile.EMPTY
                        )
        self.wall_coords = set()
        for coord in self.all_fog_objects.keys():
            for room in self.level.rooms:
                if room.is_inside(coord[0], coord[1]):
                    if coord[0] in [room.x0, room.x1] or coord[1] in [room.y0, room.y1]:
                        self.wall_coords.add(coord)

    def clear_fog(self) -> dict[tuple[int, int], GameObject]:
        player_x = self.level.player.x
        player_y = self.level.player.y

        for room in self.level.rooms:
            if room.is_inside(player_x, player_y) and not room.is_doorway(
                player_x, player_y
            ):
                self.rooms_floor_coords[room.id] = set()
                for x in range(room.x0, room.x1 + 1):
                    for y in range(room.y0, room.y1 + 1):
                        if self.rooms_floor_coords[room.id] is not None:
                            if (
                                x != room.x0
                                and x != room.x1
                                and y != room.y0
                                and y != room.y1
                            ):
                                self.rooms_floor_coords[room.id].add((x, y))
                        self.remove_fog_at(x, y)
                break
            elif room.is_inside(player_x, player_y) and room.is_doorway(
                player_x, player_y
            ):
                if self.rooms_floor_coords.get(room.id) is not None:
                    for coord in self.rooms_floor_coords[room.id]:
                        self.all_fog_objects[coord] = GameObject(
                            x=coord[0], y=coord[1], tile=Tile.EMPTY
                        )
                self.get_viewing_angle(room, player_x, player_y)
                break
            else:
                for coord in set(self.viewing_angle_coords):
                    if coord not in self.wall_coords:
                        self.all_fog_objects[coord] = GameObject(
                            x=coord[0], y=coord[1], tile=Tile.EMPTY
                        )
                    self.viewing_angle_coords.remove(coord)

        self.clear_fog_around()

        return self.all_fog_objects.values()

    def clear_fog_around(self):
        player_x = self.level.player.x
        player_y = self.level.player.y

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.remove_fog_at(player_x + dx, player_y + dy)

    def get_viewing_angle(self, room, view_x, view_y):
        self.viewing_angle_coords.clear()

        if view_x == room.x0:
            base_angle = 0
        elif view_x == room.x1:
            base_angle = 180
        elif view_y == room.y0:
            base_angle = 90
        elif view_y == room.y1:
            base_angle = 270

        fov = 90
        max_distance = max(room.x1 - room.x0, room.y1 - room.y0)

        for angle in range(base_angle - fov // 2, base_angle + fov // 2, 2):
            dx = math.cos(math.radians(angle))
            dy = math.sin(math.radians(angle))

            x, y = view_x, view_y

            for _ in range(max_distance):
                x += dx
                y += dy

                ix, iy = int(round(x)), int(round(y))

                if not room.is_inside(ix, iy):
                    break

                self.viewing_angle_coords.add((ix, iy))
                self.remove_fog_at(ix, iy)

    def remove_fog_at(self, x, y):
        for fog_obj in self.all_fog_objects.values():
            if fog_obj.x == x and fog_obj.y == y:
                del self.all_fog_objects[(fog_obj.x, fog_obj.y)]
                break
