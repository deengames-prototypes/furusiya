import colors
from game import Game
from model.helper_functions.message import message
from model.keys.in_game_decorator import in_game


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

        # TODO: DRY with key_callback movement methods?
        up_lambda = in_game(pass_turn=True)(lambda event: new_move_callback(0, -1))
        down_lambda = in_game(pass_turn=True)(lambda event: new_move_callback(0, 1))
        left_lambda = in_game(pass_turn=True)(lambda event: new_move_callback(-1, 0))
        right_lambda = in_game(pass_turn=True)(lambda event: new_move_callback(1, 0))

        Game.keybinder.register_keybinds({
            'UP': up_lambda,
            'DOWN': down_lambda,
            'LEFT': left_lambda,
            'RIGHT': right_lambda,
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

