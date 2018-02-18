import colors
from game import Game
from model.helper_functions.menu import inventory_menu
from model.helper_functions.message import message
from model.item import Item
from model.keys.in_game_decorator import in_game
from model.keys.movement_callbacks import *
from model.skills.omnislash import OmniSlash
from model.skills.whirlwind import Whirlwind
from model.config import config
from model.weapons import Bow


def exit_to_main_menu_callback(event):
    Game.save_manager.save()
    Game.ui.app.suspend()
    Game.ui.unblit_map_and_panel()


def enter_callback(event):
    if event.alt:
        Game.ui.toggle_fullscreen()


# Movement
@in_game(pass_turn=True)
def up_callback(event):
    up(Game.player.move_or_attack)


@in_game(pass_turn=True)
def down_callback(event):
    down(Game.player.move_or_attack)


@in_game(pass_turn=True)
def left_callback(event):
    left(Game.player.move_or_attack)


@in_game(pass_turn=True)
def right_callback(event):
    right(Game.player.move_or_attack)


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
@in_game(pass_turn=False)
def bow_callback(event):
    if (isinstance(Game.fighter_system.get(Game.player).weapon, Bow)
            and not config.data.features.limitedArrows
            or (config.data.features.limitedArrows and Game.player.arrows > 0)):
        Game.draw_bowsight = True
        Game.auto_target = True

        Game.keybinder.suspend_all_keybinds()

        @in_game(pass_turn=False)
        def new_escape_callback(event):
            Game.draw_bowsight = False
            Game.current_turn = Game.player
            Game.keybinder.register_all_keybinds_and_events()

        @in_game(pass_turn=True)
        def new_f_callback(event):
            if not Game.auto_target:
                Game.target = Game.area_map.get_blocking_object_at(*Game.mouse_coord) or None

            if Game.target and Game.fighter_system.has(Game.target):
                is_critical = False
                conf = config.data.weapons
                damage_multiplier = conf.arrowDamageMultiplier

                if config.data.features.bowCrits and Game.random.randint(0, 100) <= conf.bowCriticalProbability:
                    damage_multiplier *= 1 + conf.bowCriticalDamageMultiplier
                    if config.data.features.bowCritsStack:
                        target_fighter = Game.fighter_system.get(Game.target)
                        damage_multiplier += conf.bowCriticalDamageMultiplier * target_fighter.bow_crits
                        target_fighter.bow_crits += 1
                    is_critical = True

                Game.fighter_system.get(Game.player).attack(Game.target, damage_multiplier, is_critical)
                Game.player.arrows -= 1
                Game.auto_target = True

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
        turns_to_rest = Game.player.calculate_turns_to_rest()
        message(f'You rest for {turns_to_rest} turns.')

        def can_rest():
            nonlocal turns_to_rest
            return (
                turns_to_rest > 0
                and not [
                    e
                    for e in Game.area_map.entities
                    if e.hostile and (e.x, e.y) in Game.renderer.visible_tiles
                ]
            )

        def new_update_callback(delta_time):
            nonlocal turns_to_rest
            if can_rest():
                for e in Game.area_map.entities:
                    Game.ai_system.take_turn(e)
                turns_to_rest -= 1
                Game.player.rest()
            else:
                Game.keybinder.register_all_keybinds_and_events()

        Game.keybinder.suspend_all_keybinds()
        Game.keybinder.register_update(new_update_callback)


@in_game(pass_turn=True)
def whirlwind_callback(event):
    if config.data.skills.whirlwind.enabled:
        Whirlwind.process(Game.player, config.data.skills.whirlwind.radius, Game.area_map)


@in_game(pass_turn=False)
def omnislash_callback(event):
    """Enter omnislash mode!"""
    if config.data.skills.omnislash.enabled:
        message('Attack an enemy to activate omnislash, or press escape to cancel.', colors.light_cyan)

        Game.keybinder.suspend_all_keybinds()

        def new_escape_callback(event):
            message('Cancelled')
            Game.keybinder.register_all_keybinds()

        def new_move_callback(dx, dy):
            target = Game.area_map.get_blocking_object_at(Game.player.x + dx, Game.player.y + dy)
            if target is not None and Game.fighter_system.has(target):
                message(f'{target.name.capitalize()} has been ruthlessly attacked by {Game.player.name}!',
                        colors.dark_purple)
                OmniSlash.process(Game.player, target, config.data.skills.omnislash)
                new_escape_callback(None)
            else:
                Game.player.move_or_attack(dx, dy)

        @in_game(pass_turn=True)
        def new_up(event):
            up(new_move_callback)

        @in_game(pass_turn=True)
        def new_down(event):
            down(new_move_callback)

        @in_game(pass_turn=True)
        def new_left(event):
            left(new_move_callback)

        @in_game(pass_turn=True)
        def new_right(event):
            right(new_move_callback)

        Game.keybinder.register_keybinds({
            'UP': new_up,
            'DOWN': new_down,
            'LEFT': new_left,
            'RIGHT': new_right,
            'ESCAPE': new_escape_callback
        })
