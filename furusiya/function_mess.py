import shelve
from random import randint

import tdl

import colors
from model.config import config
from constants import *
from main_interface import Game, menu, message
from model.item import Item
from model.maps.area_map import AreaMap
from model.maps import generators
from model.entities.party.player import Player
from model.entities.party.stallion import Stallion
from model.maps.generators import DungeonGenerator
from model.systems.ai_system import AISystem
from model.systems.fighter_system import FighterSystem
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
        user_input = Game.ui.get_input()

    if user_input.type == 'MOUSEMOTION':
        Game.mouse_coord = user_input.cell

    if user_input.type != 'KEYDOWN':
        Game.current_turn = Game.player
        return

    # actual keybindings
    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        save_game()
        Game.playing = False
        return

    elif Game.game_state == 'playing':
        return process_in_game_keys(user_input)


def process_in_game_keys(user_input):
    Game.current_turn = None

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

        elif user_input.text == 'f' and isinstance(FighterSystem.get_fighter(Game.player).weapon, Bow):
            return process_bow()

        elif user_input.text == 'm' and Game.player.distance_to(Game.stallion) <= 1:
            Game.player.unmount(Game.stallion) if Game.player.mounted else Game.player.mount(Game.stallion)
            return ''

        elif user_input.text == 'r' and config.data.skills.resting.enabled:
            return Game.player.rest()

        elif user_input.text == 'R' and config.data.skills.resting.enabled:
            Game.player.calculate_turns_to_rest()

            def condition():
                return (
                    Game.player.turns_to_rest > 0
                    and not [
                        e
                        for e in Game.area_map.entities
                        if e.hostile and (e.x, e.y) in Game.renderer.visible_tiles
                    ]
                )

            def callback():
                for e in Game.area_map.entities:
                    AISystem.take_turn(e)
                Game.player.turns_to_rest -= 1
                Game.player.rest()

            run_loop_with(condition, callback)

        Game.current_turn = Game.player


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
                        Game.current_turn = Game.player
                        return
                    elif event.char == 'f':
                        if Game.target and FighterSystem.has_fighter(Game.target):
                            is_critical = False
                            damage_multiplier = config.data.weapons.arrowDamageMultiplier
                            if config.data.features.bowCrits and randint(0, 100) <= config.data.weapons.bowCriticalProbability:
                                damage_multiplier *= 1 + config.data.weapons.bowCriticalDamageMultiplier
                                if config.data.features.bowCritsStack:
                                    target_fighter = FighterSystem.get_fighter(Game.target)
                                    damage_multiplier += config.data.weapons.bowCriticalDamageMultiplier * target_fighter.bow_crits
                                    target_fighter.bow_crits += 1
                                is_critical = True
                            FighterSystem.get_fighter(Game.player).attack(Game.target, damage_multiplier=damage_multiplier, is_critical=is_critical)
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


def run_loop_with(condition, callback):
    while condition() and not tdl.event.is_window_closed() and Game.playing:
        Game.renderer.render()
        callback()


def play_game():

    Game.mouse_coord = (0, 0)
    Game.renderer = MapRenderer(Game.area_map, Game.player, Game.ui)
    Game.renderer.recompute_fov = True
    Game.renderer.clear()
    Game.renderer.refresh_all()

    Game.current_turn = Game.player
    Game.playing = True

    def condition():
        return not tdl.event.is_window_closed() and Game.playing

    def callback():
        if Game.current_turn is Game.player:
            handle_keys()
        else:  # it's everyone else's turn
            for e in Game.area_map.entities:
                AISystem.take_turn(e)

            Game.current_turn = Game.player

    run_loop_with(condition, callback)
