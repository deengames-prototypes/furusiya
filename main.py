#!/usr/bin/env python3

from furusiya.entities.player import Player
from furusiya.io.adapters.tdl_adapter import TdlAdapter
from furusiya.io.config_watcher import ConfigWatcher
from furusiya.io.map_renderer import MapRenderer
from furusiya.maps.area_map import AreaMap
from furusiya.maps.generators.forest_generator import ForestGenerator
import random
import time
import sys

class Main:
    # Actual size of the window
    SCREEN_WIDTH = 60
    SCREEN_HEIGHT = 40
    FPS_LIMIT = 20

    def __init__(self):
        # Just initialize variables so we can see what they all are
        self.end_game = False
        self.area_map = None
        self.player = None
        self.renderer = None


    def main(self):
        config = ConfigWatcher()

        # Hard-coded random seed for easier debugging
        random.seed(config.get("universeSeed"))

        # TODO: shouldn't use this directly here, probably.
        self.ui_adapter = TdlAdapter('Furusiya', Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT, Main.FPS_LIMIT)

        # Create the player first so monsters can refer to it
        self.player = Player()

        self.area_map = AreaMap(Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT)
        fg = ForestGenerator(Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT, self.area_map)

        self.area_map.place_on_random_ground(self.player)
        self.renderer = MapRenderer(self.area_map, self.player, self.ui_adapter)

        while not self.end_game:
            self.renderer.render()
            self.await_and_process_keyboard_input()
            self.move_enemies()

        config.dispose()

    
    def await_and_process_keyboard_input(self):
        key = self.ui_adapter.wait_for_input()
        if (key.key == "ESCAPE" or key.char.lower() == 'q'):
            self.end_game = True
        elif (key.key == "UP" and self.area_map.is_walkable(self.player.x, self.player.y - 1)):
            self.player.y -= 1
            self.renderer.recompute_fov = True
        elif (key.key == "DOWN" and self.area_map.is_walkable(self.player.x, self.player.y + 1)):
            self.renderer.recompute_fov = True
            self.player.y += 1
        elif (key.key == "LEFT" and self.area_map.is_walkable(self.player.x - 1, self.player.y)):
            self.renderer.recompute_fov = True
            self.player.x -= 1
        elif (key.key == "RIGHT" and self.area_map.is_walkable(self.player.x + 1, self.player.y)):
            self.renderer.recompute_fov = True
            self.player.x += 1


    def move_enemies(self):
        for entity in self.area_map.entities:
            try:
                entity.walk()
            except AttributeError as a:
                # AttributeError => entity isn't walkable.                
                # Ref: https://stackoverflow.com/questions/7580532/how-to-check-whether-a-method-exists-in-python
                message = str(a)
                if not "object has no attribute 'walk'" in message:
                    raise
            except ValueError as v:
                # ValueError => nothing adjacent to walk to.
                message = str(v)
                if message is not "There are no available adjacent locations":
                    raise


if __name__ == "__main__":
    Main().main()