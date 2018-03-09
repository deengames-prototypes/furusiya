import colors
from model.helper_functions.message import message
from game import Game


def monster_death(monster):
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    message(monster.name.capitalize() + ' is dead!', colors.orange)
    _mark_entity_as_dead(monster)

    Game.xp_system.get(Game.player).gain_xp(Game.xp_system.get(monster).xp)
    Game.fighter_system.remove(monster)
    Game.ai_system.remove(monster)

    monster.original_ai = None


def player_death(player):
    # the game ended!
    message('You died!', colors.red)
    Game.game_state = 'dead'
    Game.keybinder.register_all_keybinds_and_events()

    # for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = colors.dark_red


def horse_death(horse):
    message('Stallion is dead!', colors.red)
    _mark_entity_as_dead(horse)

    Game.fighter_system.remove(horse)
    Game.ai_system.remove(horse)

    if Game.player.mounted:
        Game.player.unmount(Game.stallion)


def _mark_entity_as_dead(entity):
    entity.char = '%'
    entity.color = colors.dark_red
    entity.blocks = False
    entity.name = "{} remains".format(entity.name)
    entity.send_to_back()
