from api import InputEvent

KEYMAP = {
    "w": InputEvent.MOVE_UP,
    "a": InputEvent.MOVE_LEFT,
    "s": InputEvent.MOVE_DOWN,
    "d": InputEvent.MOVE_RIGHT,
    "q": InputEvent.QUIT,
    "h": InputEvent.USE_WEAPON,
    "j": InputEvent.USE_FOOD,
    "k": InputEvent.USE_ELIXIR,
    "e": InputEvent.USE_SCROLL,
}


def read_input(key: str) -> InputEvent | None:
    return KEYMAP.get(key)
