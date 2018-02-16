from main_interface import Game


def in_game(*, pass_turn=False):
    """
    Decorator for ensuring in-game access only
    Also marks the current turn as passed.
    """
    def decorator(callback):
        def _inner_function(event):
            if Game.game_state == 'playing' and Game.current_turn is Game.player:
                if pass_turn:
                    Game.current_turn = None
                callback(event)
        return _inner_function
    return decorator
