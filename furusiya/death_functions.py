import colors
from main_interface import message
from main_interface import Game
from model.systems.ai_system import AISystem
from model.systems.fighter_system import FighterSystem
from model.systems.xp_system import XPSystem


def monster_death(monster):
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    message(monster.name.capitalize() + ' is dead!', colors.orange)
    monster.char = '%'
    monster.color = colors.dark_red
    monster.blocks = False

    XPSystem.get_experience(Game.player).gain_xp(XPSystem.get_experience(monster).xp)
    FighterSystem.remove_fighter(monster)
    AISystem.remove_ai(monster)

    monster.original_ai = None
    monster.name = "{} remains".format(monster.name)
    monster.hostile = False
    monster.send_to_back()


def player_death(player):
    # the game ended!
    message('You died!', colors.red)
    Game.game_state = 'dead'

    # for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = colors.dark_red