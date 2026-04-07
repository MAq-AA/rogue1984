import curses
import logging
import os.path

from data_layer import Reader
from game.constants import LEVEL_HEIGHT, LEVEL_WIDTH, SAVEFILE
from game.game.game import Game
from ui.main import UI

logger = logging.getLogger(__name__)
logging.basicConfig(filename="debug.log", level=logging.DEBUG, filemode="w")


def main(stdscr):
    ui = UI(width=LEVEL_WIDTH, height=LEVEL_HEIGHT)
    if os.path.exists(SAVEFILE):
        choice = ui.prompt_load()
    else:
        choice = "new"
    match choice:
        case "load":
            reader = Reader()
            game = reader.load_from_file()
            game.ui = ui
            game.loop()
        case "new":
            game = Game(ui=ui)
            game.loop()
        case "quit":
            pass


if __name__ == "__main__":
    curses.wrapper(main)
