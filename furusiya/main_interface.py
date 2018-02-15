import textwrap

import colors
from model.config import file_watcher
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, LIMIT_FPS, PANEL_HEIGHT
from constants import MSG_WIDTH, MSG_HEIGHT
from view.adapter.tdl_adapter import TdlAdapter


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

    @classmethod
    def run(cls, to_run):
        cls.ui = TdlAdapter(
            "Roguelike",
            screen=(SCREEN_WIDTH, SCREEN_HEIGHT),
            map=(MAP_WIDTH, MAP_HEIGHT),
            panel=(SCREEN_WIDTH, PANEL_HEIGHT),
            fps_limit=LIMIT_FPS
        )

        to_run()

        print("Terminating ...")

        file_watcher.stop()


def message(new_msg, color=colors.white):
    # split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        # if the buffer is full, remove the first line to make room for the new one
        if len(Game.game_msgs) == MSG_HEIGHT:
            del Game.game_msgs[0]

        # add the new line as a tuple, with the text and the color
        Game.game_msgs.append((line, color))


def get_blocking_object_at(x, y):
    for obj in Game.area_map.entities:
        if obj.blocks and obj.x == x and obj.y == y:
            return obj

    return None
