import textwrap

import colors
from constants import MSG_WIDTH, MSG_HEIGHT


class Game:
    inventory = []
    draw_bowsight = None
    player = None
    stallion = None
    mouse_coord = (0, 0)
    auto_target = None
    target = None
    game_msgs = []
    game_state = None

    area_map = None
    renderer = None
    ui = None
    current_turn = None
    playing = False  # True when in-game, false otherwise

    save_load = None
    keybinder = None


def message(new_msg, color=colors.white):
    # split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        # if the buffer is full, remove the first line to make room for the new one
        if len(Game.game_msgs) == MSG_HEIGHT:
            del Game.game_msgs[0]

        # add the new line as a tuple, with the text and the color
        Game.game_msgs.append((line, color))
