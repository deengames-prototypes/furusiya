from changquan.io.adapters.tdl_adapter import TdlAdapter
from changquan.io.config_watcher import ConfigWatcher
from changquan.generators.forest_generator import ForestGenerator
import time
import sys

#actual size of the window
SCREEN_WIDTH = 60
SCREEN_HEIGHT = 40
FPS_LIMIT = 20

ui_adapter = TdlAdapter('Changquan Dad', SCREEN_WIDTH, SCREEN_HEIGHT, FPS_LIMIT)

fg = ForestGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)

# DRAW IT!
for y in range(0, SCREEN_HEIGHT):
    for x in range(0, SCREEN_WIDTH):
        if fg.data[x][y] == True:
            char = 'T'
            colour = (0, 96, 0)
        else:
            char = '.'
            colour = (64, 48, 0)
        ui_adapter.draw(x, y, char, colour)

ui_adapter.flush()

config = ConfigWatcher()
ui_adapter.wait_for_input()

config.dispose()