from changquan.io.adapters.tdl_adapter import TdlAdapter
from changquan.io.config_watcher import ConfigWatcher
from changquan.maps.generators.forest_generator import ForestGenerator
import random
import time
import sys

config = ConfigWatcher()

# Hard-coded random seed for easier debugging
# random.seed(config.get("randomsSeed"))

#actual size of the window
SCREEN_WIDTH = 60
SCREEN_HEIGHT = 40
FPS_LIMIT = 20

ui_adapter = TdlAdapter('Changquan Dad', SCREEN_WIDTH, SCREEN_HEIGHT, FPS_LIMIT)

fg = ForestGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)
data = fg.generate_trees()

# DRAW IT!
for y in range(0, SCREEN_HEIGHT):
    for x in range(0, SCREEN_WIDTH):
        if data[x][y] == True:
            char = 'T'
            colour = (0, 96, 0)
        else:
            char = '.'
            colour = (64, 48, 0)
        ui_adapter.draw(x, y, char, colour)

ui_adapter.flush()

ui_adapter.wait_for_input()

config.dispose()