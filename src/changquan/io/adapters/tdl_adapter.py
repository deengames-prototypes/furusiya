#!/usr/bin/env python3
import tdl

class TdlAdapter:
    def __init__(self, window_title, width, height, fps_limit=20):
        tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
        self.console = tdl.init(width, height, title=window_title, fullscreen=False)
        tdl.setFPS(fps_limit)