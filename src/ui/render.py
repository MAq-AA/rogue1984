import curses
from dataclasses import fields
from typing import Iterable

from api import DisplayItem, Frame, GameStats, Tile

TILE_MAP = {
    Tile.EMPTY: " ",
    Tile.WALL_V: "\u2503",
    Tile.WALL_H: "\u2501",
    Tile.CORNER_TL: "\u250f",
    Tile.CORNER_TR: "\u2513",
    Tile.CORNER_BL: "\u2517",
    Tile.CORNER_BR: "\u251b",
    Tile.FLOOR: ".",
    Tile.CHARACTER: "@",
    Tile.CORRIDOR: "#",
    Tile.DOOR_RED: "+",
    Tile.DOOR_BLUE: "+",
    Tile.DOOR_GREEN: "+",
    Tile.ITEM_WEAPON: "/",
    Tile.ITEM_ELIXIR: "!",
    Tile.ITEM_SCROLL: "%",
    Tile.ITEM_FOOD: "*",
    Tile.ITEM_KEY_RED: "ъ",
    Tile.ITEM_KEY_BLUE: "ъ",
    Tile.ITEM_KEY_GREEN: "ъ",
    Tile.UNKNOWN: "?",
    Tile.STAIR: ">",
    Tile.MONSTER_ZOMBIE: "z",
    Tile.MONSTER_VAMPIRE: "v",
    Tile.MONSTER_GHOST: "g",
    Tile.INVISIBLE_MONSTER_GHOST: " ",
    Tile.MONSTER_OGRE: "o",
    Tile.MONSTER_SNAKE_MAGE: "s",
    Tile.MONSTER_MIMIC: "m"
}

TILE_COLORS = {
    Tile.MONSTER_ZOMBIE: curses.COLOR_GREEN,
    Tile.MONSTER_VAMPIRE: curses.COLOR_RED,
    Tile.MONSTER_OGRE: curses.COLOR_YELLOW,
    Tile.DOOR_RED: curses.COLOR_RED,
    Tile.DOOR_BLUE: curses.COLOR_BLUE,
    Tile.DOOR_GREEN: curses.COLOR_GREEN,
    Tile.ITEM_KEY_RED: curses.COLOR_RED,
    Tile.ITEM_KEY_BLUE: curses.COLOR_BLUE,
    Tile.ITEM_KEY_GREEN: curses.COLOR_GREEN,
    Tile.CHARACTER: curses.COLOR_MAGENTA,
}


def init(win):
    curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(curses.COLOR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # Do not display cursor
    curses.curs_set(False)
    win.leaveok(True)


def draw(win, frame: Frame):
    win.erase()
    for t in frame.tiles:
        char = TILE_MAP.get(t.tile, "?")
        color = TILE_COLORS.get(t.tile, 0)
        win.addstr(t.y, t.x, char, curses.color_pair(color))

    h, w = win.getmaxyx()
    message = "\n".join(frame.message.split("\n")[-4:])
    win.addstr(h - 4, 0, message)


def draw_status(win, frame: Frame):
    win.erase()

    win.addstr(f"Level: {frame.level}\n")
    win.addstr(f"HP: {frame.hp}/{frame.max_hp}+{frame.max_hp_mod}\n")
    win.addstr(f"Str: {frame.str}+{frame.str_mod}\n")
    win.addstr(f"Dex: {frame.dex}+{frame.dex_mod}\n")
    win.addstr(f"Treasure: {frame.treasure}\n")
    win.addstr(f"Weapon: {frame.weapon}\n")
    win.addstr(f"Keys: {frame.keys}\n")

    win.refresh()


def draw_stats(win, stats: GameStats):
    win.erase()

    columns = (9, 20, 29, 35, 44, 53, 62, 68, 75)
    header = (
        "Treasure",
        "Max level",
        "Enemies",
        "Food",
        "Elixirs",
        "Scrolls",
        "Attacks",
        "Hits",
        "Tiles",
    )
    for i, col in enumerate(columns):
        win.addstr(0, col - len(header[i]), header[i])
    h, w = win.getmaxyx()
    for i, run in enumerate(stats.runs):
        if i == h - 1:
            break
        for j, stat in enumerate(fields(run)):
            col = columns[j]
            value = getattr(run, stat.name)
            win.addstr(i + 1, col - len(str(value)), str(value))
    win.addstr(h - 1, 0, "Press Space to restart, or q to quit")

    win.refresh()


def choose_item(win, items: Iterable[DisplayItem], weapons=False):
    max_name_length = 20
    top = 5
    left = 20
    width = max_name_length + 10
    height = 10 + 2
    list_box = win.derwin(height, width, top, left)
    list_box.erase()
    list_box.border()
    list_box.addstr(0, 3, "item")
    list_box.addstr(0, max_name_length + 2, "value")
    i = 1
    for item in items:
        list_box.addstr(i, 1, f"{i:d}")
        list_box.addstr(i, 3, item.name)
        list_box.addstr(i, 3 + max_name_length, f"{item.stat:5d}")
        i += 1
    if weapons:
        i += 1
        list_box.addstr(i, 1, "0 unequip weapon")
    key = list_box.getkey()
    if "0" <= key <= "9":
        return int(key)
