import colors
from main_interface import message
from main_interface import Game
from model.components.ai.base import AI
from model.components.fighter import Fighter


def monster_death(monster):
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    message(monster.name.capitalize() + ' is dead!', colors.orange)
    monster.char = '%'
    monster.color = colors.dark_red
    monster.blocks = False
    Game.player.gain_xp(monster.get_component(Fighter).xp)
    monster.remove_component(Fighter)
    del monster.ai  # Relax, it's a property.
    monster.original_ai = None
    monster.name = "{} remains".format(monster.name)
    monster.send_to_back()


def player_death(player):
    # the game ended!
    message('You died!', colors.red)
    Game.game_state = 'dead'

    # for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = colors.dark_red