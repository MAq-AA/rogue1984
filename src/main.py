import curses
import logging

from game.constants import LEVEL_HEIGHT, LEVEL_WIDTH
from game.game.game import Game
from ui.main import UI

logger = logging.getLogger(__name__)
logging.basicConfig(filename="debug.log", level=logging.DEBUG, filemode="w")


def main(stdscr):
    game = Game(ui=UI(width=LEVEL_WIDTH, height=LEVEL_HEIGHT))
    # from data_layer import Reader

    # reader = Reader()
    # game = reader.load_from_file()
    game.ui = UI(width=LEVEL_WIDTH, height=LEVEL_HEIGHT)
    game.loop()


if __name__ == "__main__":
    curses.wrapper(main)
