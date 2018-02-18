import colors
from model.helper_functions.message import message
from game import Game


def monster_death(monster):
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    message(monster.name.capitalize() + ' is dead!', colors.orange)
    monster.char = '%'
    monster.color = colors.dark_red
    monster.blocks = False

    Game.xp_sys.get(Game.player).gain_xp(Game.xp_sys.get(monster).xp)
    Game.fighter_system.remove(monster)
    Game.ai_system.remove(monster)

    monster.original_ai = None
    monster.name = "{} remains".format(monster.name)
    monster.hostile = False
    monster.send_to_back()


def player_death(player):
    # the game ended!
    message('You died!', colors.red)
    Game.game_state = 'dead'
    Game.keybinder.register_all_keybinds_and_events()

    # for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = colors.dark_red