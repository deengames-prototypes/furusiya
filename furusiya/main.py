#!/usr/bin/env python3
import random
from datetime import datetime

from tcod import image_load

import colors
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, PANEL_HEIGHT, LIMIT_FPS
from game import Game
from data.saveload import SaveLoad
from model.helper_functions.menu import create_menu, message_box
from model.helper_functions.message import message
from model.config import file_watcher, config
from model.entities.party.player import Player
from model.entities.party.stallion import Stallion
from model.key_binder import KeyBinder
from model.maps import generators
from model.maps.area_map import AreaMap
from model.maps.generators import DungeonGenerator
from model.systems.xp_system import XPSystem
from view.adapter.tdl_adapter import TdlAdapter
from view.map_renderer import MapRenderer


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
    Game.game_messages = []

    # a warm welcoming message!
    message('Another brave knight yearns to bring peace to the land.', colors.red)

    # Gain four levels
    XPSystem.get_experience(Game.player).gain_xp(40 + 80 + 160 + 320)


def play_game():
    Game.ui.clear()
    Game.ui.blit_map_and_panel()

    Game.mouse_coord = (0, 0)
    Game.renderer = MapRenderer(Game.area_map, Game.player, Game.ui)
    Game.renderer.recompute_fov = True
    Game.renderer.refresh_all()

    Game.current_turn = Game.player
    Game.playing = True

    Game.ui.run()


def init_game():
    Game.ui = TdlAdapter(
        "Roguelike",
        screen=(SCREEN_WIDTH, SCREEN_HEIGHT),
        map=(MAP_WIDTH, MAP_HEIGHT),
        panel=(SCREEN_WIDTH, PANEL_HEIGHT),
        fps_limit=LIMIT_FPS
    )

    Game.save_load = SaveLoad(Game)
    Game.keybinder = KeyBinder(Game)
    Game.keybinder.register_all_keybinds_and_events()


def main_menu():
    init_game()
    img = image_load('menu_background.png')

    while not Game.ui.event_closed():
        # show the background image, at twice the regular console resolution
        img.blit_2x(Game.ui.root, 0, 0)

        # show the game's title, and some credits!
        title = 'FURUSIYA'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.ui.draw_root(center, SCREEN_HEIGHT // 2 - 4, title, colors.light_yellow)

        title = 'By nightblade9 and NegativeScript'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.ui.draw_root(center, SCREEN_HEIGHT - 2, title, colors.light_yellow)

        # show options and wait for the player's choice
        choice = create_menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  # new game
            new_game()
            play_game()
        if choice == 1:  # load last game
            try:
                Game.save_load.load()
            except Exception as e:
                message_box('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:  # quit
            break

    print("Terminating ...")

    file_watcher.stop()


if __name__ == '__main__':
    file_watcher.watch('config.json', lambda raw_json: config.load(raw_json))

    seed = config.get("seed") or int(datetime.now().timestamp())
    random.seed(seed)
    print("Seeding as universe #{}".format(seed))

    main_menu()

