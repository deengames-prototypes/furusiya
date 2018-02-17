from random import randint

from main_interface import Game
from model.inventory import inventory_menu
from model.item import Item
from model.keys.util import in_game
from model.skills.whirlwind import Whirlwind
from model.systems.ai_system import AISystem
from model.config import config
from model.systems.fighter_system import FighterSystem
from model.weapons import Bow


def exit_to_main_menu_callback(event):
    Game.saveload.save()
    Game.ui.app.suspend()


def enter_callback(event):
    if event.alt:
        Game.ui.toggle_fullscreen()


# Movement
@in_game(pass_turn=True)
def up_callback(event):
    Game.player.move_or_attack(0, -1)


@in_game(pass_turn=True)
def down_callback(event):
    Game.player.move_or_attack(0, 1)


@in_game(pass_turn=True)
def left_callback(event):
    Game.player.move_or_attack(-1, 0)


@in_game(pass_turn=True)
def right_callback(event):
    Game.player.move_or_attack(1, 0)


# Item pick up
@in_game(pass_turn=False)
def pickup_callback(event):
    for obj in Game.area_map.entities:  # look for an item in the player's tile
        obj_item = obj.get_component(Item)
        if (obj.x, obj.y) == (Game.player.x, Game.player.y) and obj_item:
            obj_item.pick_up()
            break


# Inventory use
@in_game(pass_turn=False)
def inventory_use(event):
    chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
    if chosen_item is not None:
        chosen_item.use()


# Inventory drop
@in_game(pass_turn=False)
def inventory_drop(event):
    chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
    if chosen_item is not None:
        chosen_item.drop()


# Bow
@in_game(pass_turn=True)
def bow_callback(event):
    if (isinstance(FighterSystem.get_fighter(Game.player).weapon, Bow)
            and not config.data.features.limitedArrows
            or (config.data.features.limitedArrows and Game.player.arrows > 0)):
        Game.draw_bowsight = True
        Game.auto_target = True

        Game.keybinder.suspend_all_keybinds()

        def new_escape_callback(event):
            Game.draw_bowsight = False
            Game.current_turn = Game.player
            Game.set_keybinds_and_events()

        def new_f_callback(event):
            if Game.target and FighterSystem.has_fighter(Game.target):
                is_critical = False
                conf = config.data.weapons
                damage_multiplier = conf.arrowDamageMultiplier

                if config.data.features.bowCrits and randint(0, 100) <= conf.bowCriticalProbability:
                    damage_multiplier *= 1 + conf.bowCriticalDamageMultiplier
                    if config.data.features.bowCritsStack:
                        target_fighter = FighterSystem.get_fighter(Game.target)
                        damage_multiplier += conf.bowCriticalDamageMultiplier * target_fighter.bow_crits
                        target_fighter.bow_crits += 1
                    is_critical = True

                FighterSystem.get_fighter(Game.player).attack(Game.target, damage_multiplier, is_critical)
                Game.player.arrows -= 1
                Game.draw_bowsight = False

                Game.set_keybinds_and_events()

        Game.keybinder.register_keybind('ESCAPE', new_escape_callback)
        Game.keybinder.register_keybind('f', new_f_callback)


# Mount
@in_game(pass_turn=True)
def mount_callback(event):
    if Game.player.distance_to(Game.stallion) <= 1:
        if Game.player.mounted:
            Game.player.unmount(Game.stallion)
        else:
            Game.player.mount(Game.stallion)


# Rest
@in_game(pass_turn=True)
def rest_callback(event):
    if config.data.skills.resting.enabled:
        Game.player.rest()


# Continuous rest
@in_game(pass_turn=True)
def continuous_rest_callback(event):
    if config.data.skills.resting.enabled:
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

        def callback(delta_time):
            if condition():
                for e in Game.area_map.entities:
                    AISystem.take_turn(e)
                Game.player.turns_to_rest -= 1
                Game.player.rest()
            else:
                Game.set_keybinds_and_events()

        Game.keybinder.suspend_all_keybinds()
        Game.keybinder.register_update(callback)


@in_game(pass_turn=True)
def whirlwind_callback(event):
    if config.data.skills.whirlwind.enabled:
        Whirlwind.process(Game.player, config.data.skills.whirlwind.radius, Game.area_map)
