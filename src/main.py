#!/usr/bin/env python3

from furusiya.entities.player import Player
from furusiya.io.adapters.tdl_adapter import TdlAdapter
from furusiya.io.config_watcher import ConfigWatcher
from furusiya.maps.map import Map
from furusiya.maps.generators.forest_generator import ForestGenerator
import random
import time
import sys

class Main:
    # Actual size of the window
    SCREEN_WIDTH = 60
    SCREEN_HEIGHT = 40
    FPS_LIMIT = 20

    def main(self):
        config = ConfigWatcher()

        # Hard-coded random seed for easier debugging
        random.seed(config.get("universeSeed"))
        ui_adapter = TdlAdapter('Furusiya', Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT, Main.FPS_LIMIT)

        end_game = False

        while not end_game:
            map = Map(Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT)
            fg = ForestGenerator(Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT)
            fg.generate_trees(map)

            player = Player()
            map.place_on_random_ground(player)

            # DRAW IT!
            for y in range(0, map.height):
                for x in range(0, map.width):
                    tile = map.tiles[x][y]
                    ui_adapter.draw(x, y, tile.character, tile.colour)

            for e in map.entities:
                ui_adapter.draw(e.x, e.y, e.character, e.colour)

            ui_adapter.flush()

            key = ui_adapter.wait_for_input()
            if (key.key == "ESCAPE" or key.char.lower() == 'q'):
                end_game = True

        config.dispose()


if __name__ == "__main__":
    Main().main()