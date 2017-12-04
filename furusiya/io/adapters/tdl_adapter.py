#!/usr/bin/env python3
import tdl

class TdlAdapter:
    def __init__(self, window_title, width, height, fps_limit=20):
        tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
        self.console = tdl.init(width, height, title=window_title, fullscreen=False)
        tdl.setFPS(fps_limit)


    # TODO: maybe we don't want this design ...
    def draw(self, x, y, char, colour):
        self.console.draw_str(x, y, char, colour, bg=None)


    def flush(self):
        # draw on-screen
        tdl.flush()

    def calculate_fov(self, origin_x, origin_y, is_tile_walkable_callback, algorithm, view_radius, should_light_walls):
        return tdl.map.quickFOV(origin_x, origin_y,
            is_tile_walkable_callback,
            fov=algorithm,
            radius=view_radius,
            lightWalls=should_light_walls)

    def wait_for_input(self):
        # wait for response
        key = tdl.event.key_wait()
        return key


    # Ask for input. If none, returns None.
    def get_input(self):
        keypress = False
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                print("KEY DOWN: {0}".format(event))
                return event # contains key pressed
            if event.type == 'MOUSEMOTION':
                print("MOUSE: {0}".format(event))
                return event.cell
    
        if not keypress:
            return None