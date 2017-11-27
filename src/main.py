#!/usr/bin/env python3

from changquan.io.adapters.tdl_adapter import TdlAdapter
from changquan.io.config_watcher import ConfigWatcher
from changquan.maps.map import Map
from changquan.maps.generators.forest_generator import ForestGenerator
import random
import time
import sys

def main():
    config = ConfigWatcher()

    # Hard-coded random seed for easier debugging
    random.seed(config.get("universeSeed"))

    #actual size of the window
    SCREEN_WIDTH = 60
    SCREEN_HEIGHT = 40
    FPS_LIMIT = 20

    ui_adapter = TdlAdapter('Changquan Dad', SCREEN_WIDTH, SCREEN_HEIGHT, FPS_LIMIT)

    end_game = False

    while not end_game:
        map = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
        fg = ForestGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)
        fg.generate_trees(map)

        # DRAW IT!
        for y in range(0, map.height):
            for x in range(0, map.width):
                tile = map.tiles[x][y]
                ui_adapter.draw(x, y, tile.character, tile.colour)

        ui_adapter.flush()

        key = ui_adapter.wait_for_input()
        if (key.key == "ESCAPE" or key.char.lower() == 'q'):
            end_game = True

    config.dispose()


if __name__ == "__main__":
    main()