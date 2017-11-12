#!/usr/bin/env python3
import tdl

class TdlAdapter:
    def __init__(self, window_title, width, height, fps_limit=20):
        tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
        self.console = tdl.init(width, height, title=window_title, fullscreen=False)
        tdl.setFPS(fps_limit)

    # TODO: maybe we don't want this design ...
    def draw_walls(self, data):
        width = len(data)
        height = len(data[0])

        for y in range(0, height):
            for x in range(0, width):
                if data[x][y] == True:
                    char = 'T'
                    fg = (0, 128, 0)
                else:
                    char = '.'
                    fg = (0, 64, 0)
                self.console.draw_str(x, y, char, fg, bg=None)

        # draw on-screen
        tdl.flush()
        # wait for response
        key = tdl.event.key_wait()