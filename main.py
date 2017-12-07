#!/usr/bin/env python3

from furusiya.entities.player import Player
from furusiya.io.adapters.tdl_adapter import TdlAdapter
from furusiya.io.config_watcher import ConfigWatcher
from furusiya.io.map_renderer import MapRenderer
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

        # TODO: shouldn't use this directly here, probably.
        ui_adapter = TdlAdapter('Furusiya', Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT, Main.FPS_LIMIT)

        end_game = False

        map = Map(Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT)
        fg = ForestGenerator(Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT)
        fg.generate(map)

        player = Player()
        map.place_on_random_ground(player)
        renderer = MapRenderer(map, player, ui_adapter)

        while not end_game:
            renderer.render()
            key = ui_adapter.wait_for_input()
            if (key.key == "ESCAPE" or key.char.lower() == 'q'):
                end_game = True
            elif (key.key == "UP" and map.is_walkable(player.x, player.y - 1)):
                player.y -= 1
                renderer.recompute_fov = True
            elif (key.key == "DOWN" and map.is_walkable(player.x, player.y + 1)):
                renderer.recompute_fov = True
                player.y += 1
            elif (key.key == "LEFT" and map.is_walkable(player.x - 1, player.y)):
                renderer.recompute_fov = True
                player.x -= 1
            elif (key.key == "RIGHT" and map.is_walkable(player.x + 1, player.y)):
                renderer.recompute_fov = True
                player.x += 1

        config.dispose()

if __name__ == "__main__":
    Main().main()