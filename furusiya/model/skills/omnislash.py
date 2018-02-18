import colors
from game import Game
from model.helper_functions.message import message
from model.keys.in_game_decorator import in_game
from model.keys.movement_callbacks import *


class OmniSlash:
    @classmethod
    def process(cls, player, conf):
        message('Attack an enemy to activate omnislash, or press escape to cancel.', colors.light_cyan)

        Game.keybinder.suspend_all_keybinds()

        def new_escape_callback(event):
            Game.keybinder.register_all_keybinds()

        def new_move_callback(dx, dy):
            target = Game.area_map.get_blocking_object_at(player.x + dx, player.y + dy)
            if target is not None and Game.fighter_system.has(target):
                cls.slash(player, target, conf)
                new_escape_callback(None)
            else:
                player.move_or_attack(dx, dy)

        up_lambda = lambda ev: up(new_move_callback)
        down_lambda = lambda ev: down(new_move_callback)
        left_lambda = lambda ev: left(new_move_callback)
        right_lambda = lambda ev: right(new_move_callback)

        Game.keybinder.register_keybinds({
            'UP': in_game(up_lambda, pass_turn=True),
            'DOWN': in_game(down_lambda, pass_turn=True),
            'LEFT': in_game(left_lambda, pass_turn=True),
            'RIGHT': in_game(right_lambda, pass_turn=True),
            'ESCAPE': new_escape_callback
        })

    @classmethod
    def slash(cls, player, target, conf):
        # do guaranteed hits
        for _ in range(conf.guaranteedHits):
            if Game.fighter_system.has(target):
                Game.fighter_system.get(player).attack(target)
            else:
                return  # it's dead already!

        # do lucky hits
        while True:
            should_re_hit = Game.random.randint(0, 100) <= conf.rehitPercent
            if should_re_hit and Game.fighter_system.has(target):
                Game.fighter_system.get(player).attack(target)
            else:
                return

