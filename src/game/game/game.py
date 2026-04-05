from enum import Enum, auto

from api import DrawTile, Frame, InputEvent, Tile
from game.constants import MAX_DEPTH
from game.entities.character import Character
from game.game.level import Level
from game.items import Elixir, Food, Key, Scroll, Weapon, fist
from stat_tracker import stat_tracker
from game.game.fog_of_war import FogOfWar


class GameStatus(Enum):
    ACTIVE = auto()
    WON = auto()
    LOST = auto()


class Game:
    def __init__(self, ui):
        self.ui = ui
        self.current_depth = 1
        self.level = Level(depth=self.current_depth, player=Character())
        self.game_status = GameStatus.ACTIVE
        self.fog_of_war = FogOfWar(self.level)
        self.quit = False

    def loop(self):
        self.ui.draw(self.frame())
        while not self.quit:
            event = self.ui.get_input()
            if event == InputEvent.QUIT:
                self.quit = True
            if event is not None:
                self.handle(event)
                self.get_current_game_status()
                self.do_action_by_game_status()
                self.ui.draw(self.frame())

    def get_current_game_status(self):
        if self.level.player.hp <= 0:
            self.game_status = GameStatus.LOST
        elif self.current_depth > MAX_DEPTH:
            self.game_status = GameStatus.WON
        elif self.level.exited:
            self.advance_depth()

    def do_action_by_game_status(self):
        if self.game_status == GameStatus.WON:
            pass
            # TODO present winner screen
        elif self.game_status == GameStatus.LOST:
            stat_tracker.write_stats()
            if self.ui.game_over(stat_tracker.load_stats()):
                self.quit = True

        # TODO add function to save score in high score table
        if self.game_status in [GameStatus.WON, GameStatus.LOST]:
            self.current_depth = 1
            self.level = Level(depth=self.current_depth, player=Character())
            self.game_status = GameStatus.ACTIVE

    def handle(self, event: InputEvent):
        if self.level.player.is_stunned:
            self.level.player.is_stunned = False
            self.level.end_turn()
            return None
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
                    [x.display_item() for x in backpack.find_all(Weapon)],
                    weapons=True,
                )
                if player.weapon != fist:
                    if item_id:
                        level.drop(player.weapon)
                player.equip(item_id)

            case InputEvent.USE_FOOD:
                item_id = self.ui.choose_item(
                    [x.display_item() for x in backpack.find_all(Food)]
                )
                if item_id:
                    player.use_food(item_id)

            case InputEvent.USE_ELIXIR:
                item_id = self.ui.choose_item(
                    [x.display_item() for x in backpack.find_all(Elixir)]
                )
                if item_id:
                    player.use_elixir(item_id)

            case InputEvent.USE_SCROLL:
                item_id = self.ui.choose_item(
                    [x.display_item() for x in backpack.find_all(Scroll)]
                )
                if item_id:
                    player.use_scroll(item_id)

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
            else:
                for x in range(room.x0 + 1, room.x1):
                    for y in range(room.y0 + 1, room.y1):
                        tiles.append(DrawTile(x, y, Tile.EMPTY))
        return tiles

    def draw_corridors(self) -> list[DrawTile]:
        tiles = []
        for c in self.level.corridors:
            for x in range(min(c.x0, c.x1), max(c.x0, c.x1) + 1):
                for y in range(min(c.y0, c.y1), max(c.y0, c.y1) + 1):
                    if c.is_inside(x, y):
                        if c.door(x, y) and c.closed:
                            tiles.append(DrawTile(x, y, c.closed.tile))
                        else:
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
        tiles.extend(self.fog_of_war.clear_fog())
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
            weapon=player.weapon.display_item().name,
            keys=", ".join([x.color.value for x in player.backpack.find_all(Key)]),
        )
        self.level.message = ""
        return ret

    def advance_depth(self):
        self.current_depth += 1
        self.level = Level(depth=self.current_depth, player=self.level.player)
        self.fog_of_war = FogOfWar(self.level)
        player = self.level.player
        player.remove_bonuses()
        player.remove_keys()
        stat_tracker.level = self.current_depth
