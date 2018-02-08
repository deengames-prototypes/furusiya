#!/usr/bin/env python3
import tdl
from tcod import image_load
import colors

# Has to be here, because we use it everywhere
from model.config import file_watcher, config
file_watcher.watch('config.json', lambda raw_json: config.load(raw_json))

from function_mess import new_game, play_game, load_game, msgbox
from main_interface import Game, menu
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import random

def main_menu():
    img = image_load('menu_background.png')

    while not tdl.event.is_window_closed():
        # show the background image, at twice the regular console resolution
        img.blit_2x(Game.ui.root, 0, 0)

        # show the game's title, and some credits!
        title = 'FURUSIYA'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.ui.root.draw_str(center, SCREEN_HEIGHT // 2 - 4, title, bg=None, fg=colors.light_yellow)

        title = 'By nightblade9 and NegativeScript'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.ui.root.draw_str(center, SCREEN_HEIGHT - 2, title, bg=None, fg=colors.light_yellow)

        # show options and wait for the player's choice
        choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  # new game
            new_game()
            play_game()
        if choice == 1:  # load last game
            try:
                load_game()
            except:
                msgbox('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:  # quit
            break

if config.has("seed"):
    seed = config.get("seed")
    random.seed(seed)
    print("Seeding as universe #{}".format(seed))
Game.run(main_menu)
