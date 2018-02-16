#!/usr/bin/env python3
from datetime import datetime

from tcod import image_load
import colors

# Has to be here, because we use it everywhere
from model.config import file_watcher, config

file_watcher.watch('config.json', lambda raw_json: config.load(raw_json))

from view.map_renderer import MapRenderer
from model.entities.party.player import Player
from model.entities.party.stallion import Stallion
from model.maps import generators
from model.maps.area_map import AreaMap
from model.maps.generators import DungeonGenerator
from main_interface import Game, message
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT
import random


def new_game():

    Game.area_map = AreaMap(MAP_WIDTH, MAP_HEIGHT)
    Game.player = Player()
    Game.stallion = Stallion(Game.player)

    # generate map (at this point it's not drawn to the screen)
    generator_class_name = f'{str(config.data.mapType).lower().capitalize()}Generator'
    generator = getattr(generators, generator_class_name, DungeonGenerator)
    generator(Game.area_map)

    Game.area_map.place_on_random_ground(Game.player)
    # TODO: what if we spawned in a wall? :/
    Game.stallion.x = Game.player.x + 1
    Game.stallion.y = Game.player.y + 1
    Game.area_map.entities.append(Game.stallion)

    Game.game_state = 'playing'
    Game.inventory = []

    # create the list of game messages and their colors, starts empty
    Game.game_msgs = []

    # a warm welcoming message!
    message('Another brave knight yearns to bring peace to the land.', colors.red)

    # Gain four levels
    Game.player.gain_xp(40 + 80 + 160 + 320)


def play_game():
    Game.mouse_coord = (0, 0)
    Game.renderer = MapRenderer(Game.area_map, Game.player, Game.ui)
    Game.renderer.recompute_fov = True
    Game.renderer.clear()
    Game.renderer.refresh_all()

    Game.current_turn = Game.player
    Game.playing = True
    Game.ui.run()


def main_menu():
    img = image_load('menu_background.png')
    Game.set_keybinds_and_events()

    while not Game.ui.event_closed():
        # show the background image, at twice the regular console resolution
        img.blit_2x(Game.ui.root, 0, 0)

        # show the game's title, and some credits!
        title = 'FURUSIYA'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.ui.draw_string(center, SCREEN_HEIGHT // 2 - 4, title, colors.light_yellow)

        title = 'By nightblade9 and NegativeScript'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.ui.draw_string(center, SCREEN_HEIGHT - 2, title, colors.light_yellow)

        # show options and wait for the player's choice
        choice = Game.ui.create_menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  # new game
            new_game()
            play_game()
        if choice == 1:  # load last game
            try:
                Game.saveload.load()
            except Exception as e:
                Game.ui.message_box('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:  # quit
            break


seed = config.get("seed") or int(datetime.now().timestamp())
random.seed(seed)
print("Seeding as universe #{}".format(seed))

Game.run(main_menu)
