from enum import Enum, auto

from api import DrawTile, Frame, InputEvent, Tile
from game.entities.character import Character
from game.game.level import Level
from game.items import Elixir, Food, Scroll, Weapon, fist


class GameStatus(Enum):
    ACTIVE = auto()
    WON = auto()
    LOST = auto()


class Game:
    MAX_DEPTH: int = 21

    def __init__(self, ui):
        self.ui = ui
        self.current_depth = 1
        self.level = Level(depth=self.current_depth, player=Character())
        self.game_status = GameStatus.ACTIVE

    def loop(self):
        self.ui.draw(self.frame())
        while True:
            event = self.ui.get_input()
            if event == InputEvent.QUIT:
                break
            if event is not None:
                self.handle(event)
                self.get_current_game_status()
                self.do_action_by_game_status()
                self.ui.draw(self.frame())

    def get_current_game_status(self):
        if self.level.player.hp <= 0:
            self.game_status = GameStatus.LOST
        elif self.current_depth > Game.MAX_DEPTH:
            self.game_status = GameStatus.WON
        elif self.level.exited:
            self.advance_depth()

    def do_action_by_game_status(self):
        if self.game_status == GameStatus.WON:
            pass
            # TODO present winner screen
        elif self.game_status == GameStatus.LOST:
            pass
            # TODO present loser screen

        # TODO add function to save score in high score table

    def handle(self, event: InputEvent):
        level = self.level
        player = level.player
        backpack = player.backpack
        match event:
            case InputEvent.MOVE_UP:
                level.move(player, dy=-1)
                level.end_turn()
            case InputEvent.MOVE_DOWN:
                level.move(player, dy=1)
                level.end_turn()
            case InputEvent.MOVE_LEFT:
                level.move(player, dx=-1)
                level.end_turn()
            case InputEvent.MOVE_RIGHT:
                level.move(player, dx=1)
                level.end_turn()
            case InputEvent.USE_WEAPON:
                item_id = self.ui.choose_item(
                    [x.display_item() for x in backpack.items if isinstance(x, Weapon)],
                    weapons=True,
                )
                if item_id:
                    item = next(x for x in backpack.items if id(x) == item_id)
                    player.weapon = item
                    backpack.remove(item)
                elif item_id == 0:
                    if player.weapon != fist and backpack.put(player.weapon):
                        player.weapon = fist

            case InputEvent.USE_FOOD:
                item_id = self.ui.choose_item(
                    [x.display_item() for x in backpack.items if isinstance(x, Food)]
                )
                if item_id:
                    item = next(x for x in backpack.items if id(x) == item_id)
                    player.hp = min(
                        player.hp + item.hp, player.max_hp + player.max_hp_mod
                    )
                    backpack.remove(item)
            case InputEvent.USE_ELIXIR:
                item_id = self.ui.choose_item(
                    [x.display_item() for x in backpack.items if isinstance(x, Elixir)]
                )
                if item_id:
                    item = next(x for x in backpack.items if id(x) == item_id)
                    player.max_hp_mod += item.max_hp
                    player.hp += item.max_hp
                    player.str_mod += item.str_
                    player.dex_mod += item.dex
                    backpack.remove(item)
            case InputEvent.USE_SCROLL:
                item_id = self.ui.choose_item(
                    [x.display_item() for x in backpack.items if isinstance(x, Scroll)]
                )
                if item_id:
                    item = next(x for x in backpack.items if id(x) == item_id)
                    player.max_hp += item.max_hp
                    player.hp += item.max_hp
                    player.str += item.str_
                    player.dex += item.dex
                    backpack.remove(item)

    def in_room(self, room, x: int, y: int) -> bool:
        return room.x0 <= x <= room.x1 and room.y0 <= y <= room.y1

    def draw_rooms(self) -> list[DrawTile]:
        tiles = []
        for room in self.level.rooms:
            for x in range(room.x0, room.x1 + 1):
                tiles.append(DrawTile(x, room.y0, Tile.WALL_H))
                tiles.append(DrawTile(x, room.y1, Tile.WALL_H))
            for y in range(room.y0 + 1, room.y1):
                tiles.append(DrawTile(room.x0, y, Tile.WALL_V))
                tiles.append(DrawTile(room.x1, y, Tile.WALL_V))
            tiles.append(DrawTile(room.x0, room.y0, Tile.CORNER_TL))
            tiles.append(DrawTile(room.x0, room.y1, Tile.CORNER_BL))
            tiles.append(DrawTile(room.x1, room.y0, Tile.CORNER_TR))
            tiles.append(DrawTile(room.x1, room.y1, Tile.CORNER_BR))
            if self.in_room(room, *self.level.player.coords):
                for x in range(room.x0 + 1, room.x1):
                    for y in range(room.y0 + 1, room.y1):
                        tiles.append(DrawTile(x, y, Tile.FLOOR))
        return tiles

    def draw_corridors(self) -> list[DrawTile]:
        tiles = []
        for c in self.level.corridors:
            for x in range(min(c.x0, c.x1), max(c.x0, c.x1) + 1):
                for y in range(min(c.y0, c.y1), max(c.y0, c.y1) + 1):
                    if c.is_inside(x, y):
                        tiles.append(DrawTile(x, y, Tile.CORRIDOR))
        return tiles

    def frame(self) -> Frame:
        player = self.level.player
        tiles = []
        tiles.extend(self.draw_rooms())
        tiles.extend(self.draw_corridors())
        tiles.extend(
            DrawTile(obj.x, obj.y, obj.tile)
            for obj in self.level.monsters + self.level.items
        )
        tiles.append(DrawTile(player.x, player.y, Tile.CHARACTER))
        tiles.append(DrawTile(self.level.stair.x, self.level.stair.y, Tile.STAIR))
        ret = Frame(
            tiles=tiles,
            hp=player.hp,
            max_hp=player.max_hp,
            max_hp_mod=player.max_hp_mod,
            str=player.str,
            str_mod=player.str_mod,
            dex=player.dex,
            dex_mod=player.dex_mod,
            treasure=player.treasure,
            level=self.level.depth,
            message=self.level.message,
            weapon=player.weapon.name,
        )
        self.level.message = ""
        return ret

    def advance_depth(self):
        self.current_depth += 1
        self.level = Level(depth=self.current_depth, player=self.level.player)
        player = self.level.player
        player.hp = max(1, player.hp - player.max_hp_mod)
        player.max_hp_mod = 0
        player.str_mod = 0
        player.dex_mod = 0
