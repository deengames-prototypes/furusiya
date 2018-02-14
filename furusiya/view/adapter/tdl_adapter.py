#!/usr/bin/env python3
import textwrap

import tdl

import colors
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from model.config import config


class TdlAdapter:
    def __init__(self, window_title, screen, map, panel, fps_limit=20):
        tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
        self.root = tdl.init(*screen, title=window_title,
                             fullscreen=config.data.fullscreen)
        tdl.setFPS(fps_limit)
        self.con = tdl.Console(*map)
        self.panel = tdl.Console(*panel)

    def clear(self):
        """
        Clears the screen.
        """
        self.con.clear()

    @staticmethod
    def flush():
        """
        Render everything from buffers to screen
        """
        tdl.flush()

    @staticmethod
    def calculate_fov(origin_x, origin_y, is_tile_walkable_callback, algorithm, view_radius, should_light_walls):
        return tdl.map.quickFOV(
            origin_x, origin_y,
            is_tile_walkable_callback,
            fov=algorithm,
            radius=view_radius,
            lightWalls=should_light_walls
        )

    @staticmethod
    def wait_for_input():
        """
        wait for response
        """
        key = tdl.event.key_wait()
        return key

    @staticmethod
    def get_input():
        """
        Ask for input. If none, returns None.
        """
        keypress = False
        for event in tdl.event.get():
            return event
    
        if not keypress:
            return None

    @staticmethod
    def toggle_fullscreen():
        tdl.set_fullscreen(not tdl.get_fullscreen())

    @staticmethod
    def event_closed():
        return tdl.event.is_window_closed()

    def draw_string(self, x, y, string, color):
        self.root.draw_str(x, y, string, bg=None, fg=color)

    def create_menu(self, header, options, width):
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

        # blit the contents of "window" to the Game.ui.root console
        x = SCREEN_WIDTH // 2 - width // 2
        y = SCREEN_HEIGHT // 2 - height // 2
        self.root.blit(window, x, y, width, height, 0, 0, fg_alpha=1.0, bg_alpha=0.7)

        # present the Game.ui.root console to the player and wait for a key-press
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

    def message_box(self, text, width=50):
        self.create_menu(text, [], width)

    def bresenham(self, x1, y1, x2, y2):
        return tdl.map.bresenham(x1, y1, x2, y2)