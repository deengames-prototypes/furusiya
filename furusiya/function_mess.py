import shelve
from random import randint

import tdl

import colors
from model.config import config
from constants import *
from main_interface import Game, menu, message
from model.components.fighter import Fighter
from model.entities.npc import NPC
from model.item import Item
from model.maps.area_map import AreaMap
from model.maps import generators
from model.entities.party.player import Player
from model.entities.party.stallion import Stallion
from model.maps.generators import DungeonGenerator
from model.weapons import Bow
from view.map_renderer import MapRenderer


def inventory_menu(header):
    # show a menu with each item of the inventory as an option
    if len(Game.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in Game.inventory]

    index = menu(header, options, INVENTORY_WIDTH)

    # if an item was chosen, return it
    if index is None or len(Game.inventory) == 0:
        return None
    return Game.inventory[index].get_component(Item)


def msgbox(text, width=50):
    menu(text, [], width)  # use menu() as a sort of "message box"


def handle_keys():
    user_input = None
    while user_input is None:
        # Synchronously wait
        for event in tdl.event.get():
            if event is not None:
                user_input = event

    if user_input.type == 'MOUSEMOTION':
        Game.mouse_coord = user_input.cell

    if user_input.type != 'KEYDOWN':
        return 'didnt-take-turn'

    # actual keybindings
    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return 'exit'  # exit game

    elif Game.game_state == 'playing':
        return process_in_game_keys(user_input)


def process_in_game_keys(user_input):
    # movement keys
    if user_input.key == 'UP':
        Game.player.move_or_attack(0, -1)

    elif user_input.key == 'DOWN':
        Game.player.move_or_attack(0, 1)

    elif user_input.key == 'LEFT':
        Game.player.move_or_attack(-1, 0)

    elif user_input.key == 'RIGHT':
        Game.player.move_or_attack(1, 0)
    else:
        # test for other keys
        if user_input.text == 'g':
            # pick up an item
            for obj in Game.area_map.entities:  # look for an item in the player's tile
                obj_item = obj.get_component(Item)
                if (obj.x, obj.y) == (Game.player.x, Game.player.y) and obj_item:
                    obj_item.pick_up()
                    break

        elif user_input.text == 'i':
            # show the inventory; if an item is selected, use it
            chosen_item = inventory_menu('Press the key next to an item to ' +
                                         'use it, or any other to cancel.\n')
            if chosen_item is not None:
                chosen_item.use()

        elif user_input.text == 'd':
            # show the inventory; if an item is selected, drop it
            chosen_item = inventory_menu('Press the key next to an item to' +
                                         'drop it, or any other to cancel.\n')
            if chosen_item is not None:
                chosen_item.drop()

        elif user_input.text == 'f' and isinstance(Game.player.get_component(Fighter).weapon, Bow):
            return process_bow()

        return 'didnt-take-turn'


def process_bow():
    # Unlimited arrows, or limited but we have arrows
    if not config.data.features.limitedArrows or (config.data.features.limitedArrows and Game.player.arrows > 0):
        Game.draw_bowsight = True
        Game.auto_target = True
        Game.renderer.render()  # show default targetting
        while True:
            for event in tdl.event.get():
                if event.type == 'MOUSEMOTION':
                    Game.mouse_coord = event.cell
                    Game.auto_target = False
                    Game.renderer.render()
                elif event.type == 'KEYDOWN':
                    if event.key == 'ESCAPE':
                        Game.draw_bowsight = False
                        break
                    elif event.char == 'f':
                        if Game.target and Game.target.has_component(Fighter):
                            is_critical = False
                            damage_multiplier = config.data.weapons.arrowDamageMultiplier
                            if config.data.features.bowCrits and randint(0, 100) <= config.data.weapons.bowCriticalProbability:
                                damage_multiplier *= 1 + config.data.weapons.bowCriticalDamageMultiplier
                                if config.data.features.bowCritsStack:
                                    target_fighter = Game.target.get_component(Fighter)
                                    damage_multiplier += config.data.weapons.bowCriticalDamageMultiplier * target_fighter.bow_crits
                                    target_fighter.bow_crits += 1
                                is_critical = True
                            Game.player.get_component(Fighter).attack(Game.target, damage_multiplier=damage_multiplier, is_critical=is_critical)
                            Game.player.arrows -= 1
                            Game.draw_bowsight = False
                            return ""


def save_game():
    # open a new empty shelve (possibly overwriting an old one) to write the game data
    with shelve.open('savegame', 'n') as savefile:
        savefile['tiles'] = Game.area_map.tiles
        savefile['entities'] = Game.area_map.entities
        savefile['player_index'] = Game.area_map.entities.index(Game.player)  # index of player in entities list
        savefile['inventory'] = Game.inventory
        savefile['game_msgs'] = Game.game_msgs
        savefile['game_state'] = Game.game_state


def load_game():
    # open the previously saved shelve and load the game data

    with shelve.open('savegame', 'r') as savefile:
        Game.area_map.tiles = savefile['tiles']
        Game.area_map.width = len(Game.area_map.tiles)
        Game.area_map.height = len(Game.area_map.tiles[0])
        Game.area_map.entities = savefile['entities']
        Game.player = Game.area_map.entities[savefile['player_index']]  # get index of player in objects list and access it
        Game.inventory = savefile['inventory']
        Game.game_msgs = savefile['game_msgs']
        Game.game_state = savefile['game_state']


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

    player_action = None
    Game.mouse_coord = (0, 0)
    Game.renderer = MapRenderer(Game.area_map, Game.player, Game.ui)
    Game.renderer.recompute_fov = True
    Game.renderer.refresh_all()

    while not tdl.event.is_window_closed():
        # draw all objects in the list
        Game.renderer.render()

        # handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break

        # let monsters take their turn
        if Game.game_state == 'playing' and player_action != 'didnt-take-turn':
            for obj in Game.area_map.entities:
                if not isinstance(obj, NPC):
                    continue
                obj_ai = obj.ai
                if obj_ai:
                    obj_ai.take_turn()
