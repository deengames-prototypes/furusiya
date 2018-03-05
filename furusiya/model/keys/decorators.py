from functools import wraps

import colors
from game import Game
from model.helper_functions.message import message


def in_game(callback=None, *, pass_turn=False):
    """
    Decorator for ensuring in-game access only
    Also marks the current turn as passed.
    """
    def decorator(callback):
        @wraps(callback)
        def _inner_function(event):
            if Game.game_state == 'playing' and Game.current_turn is Game.player:
                if pass_turn:
                    Game.current_turn = None
                callback(event)

        return _inner_function

    if callback is None:
        return decorator
    else:
        return decorator(callback)


def skill(callback=None, *, cost=0):
    def decorator(callback):
        @wraps(callback)
        def _inner_function(event):
            if Game.player.can_use_skill(cost):
                Game.player.use_skill(cost)
                callback(event)
            else:
                message(f"Not enough skill points to use skill!", colors.dark_red)

        return _inner_function

    if callback is None:
        return decorator
    else:
        return decorator(callback)
