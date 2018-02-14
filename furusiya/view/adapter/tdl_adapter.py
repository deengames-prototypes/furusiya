#!/usr/bin/env python3
import tdl
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
