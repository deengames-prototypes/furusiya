import textwrap

import tdl

import colors
import file_watcher
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LIMIT_FPS, MAP_WIDTH
from constants import MAP_HEIGHT, PANEL_HEIGHT, MSG_WIDTH, MSG_HEIGHT
from model.maps.area_map import AreaMap


class Game:
    root = None
    con = None
    panel = None
    inventory = []
    visible_tiles = None
    draw_bowsight = None
    player = None
    stallion = None
    fov_recompute = None
    mouse_coord = None
    auto_target = None
    target = None
    game_msgs = []
    game_state = None

    area_map: AreaMap = None

    @classmethod
    def run(cls, to_run):
        tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
        cls.root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike",
                            fullscreen=False)
        tdl.setFPS(LIMIT_FPS)
        cls.con = tdl.Console(MAP_WIDTH, MAP_HEIGHT)
        cls.panel = tdl.Console(SCREEN_WIDTH, PANEL_HEIGHT)

        to_run()

        print("Terminating ...")

        file_watcher.stop()


def menu(header, options, width):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after textwrap) and one line per option
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tdl.Console(width, height)

    # print the header, with wrapped text
    window.draw_rect(0, 0, width, height, None, fg=colors.white, bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.draw_str(0, y, text, bg=None)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the Game.root console
    x = SCREEN_WIDTH // 2 - width // 2
    y = SCREEN_HEIGHT // 2 - height // 2
    Game.root.blit(window, x, y, width, height, 0, 0, fg_alpha=1.0, bg_alpha=0.7)

    # present the Game.root console to the player and wait for a key-press
    tdl.flush()
    key = tdl.event.key_wait()
    key_char = key.char
    if key_char == '':
        key_char = ' '  # placeholder

    if key.key == 'ENTER' and key.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    # convert the ASCII code to an index; if it corresponds to an option, return it
    index = ord(key_char) - ord('a')
    if 0 <= index < len(options):
        return index
    return None


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
