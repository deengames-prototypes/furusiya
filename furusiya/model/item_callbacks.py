import colors
from constants import HEAL_AMOUNT, LIGHTNING_RANGE, LIGHTNING_DAMAGE, CONFUSE_RANGE, FIREBALL_RADIUS, FIREBALL_DAMAGE
from view.targeting_distance import target_tile, target_monster
from view.targeting_monster import closest_monster
from main_interface import Game, message
from model.components.ai.monster import ConfusedMonster
from model.components.fighter import Fighter


def cast_heal():
    # heal the player
    player_fighter = Game.player.get_component(Fighter)
    if player_fighter.hp == player_fighter.max_hp:
        message('You are already at full health.', colors.red)
        return 'cancelled'

    message('Your wounds start to feel better!', colors.light_violet)
    player_fighter.heal(HEAL_AMOUNT)


def cast_lightning():
    # find closest enemy (inside a maximum range) and damage it
    monster = closest_monster(LIGHTNING_RANGE)
    if monster is None:  # no enemy found within maximum range
        message('No enemy is close enough to strike.', colors.red)
        return 'cancelled'

    # zap it!
    message('A lighting bolt strikes the ' + monster.name + ' with a loud ' +
            'thunder! The damage is ' + str(LIGHTNING_DAMAGE) + ' hit points.',
            colors.light_blue)

    monster.get_component(Fighter).take_damage(LIGHTNING_DAMAGE)


def cast_confuse():
    # ask the player for a target to confuse
    message('Left-click an enemy to confuse it, or right-click to cancel.',
            colors.light_cyan)
    monster = target_monster(CONFUSE_RANGE)
    if monster is None:
        message('Cancelled')
        return 'cancelled'

    # replace the monster's AI with a "confused" one; after some turns it will
    # restore the old AI
    monster.set_ai(ConfusedMonster(monster))
    message('The eyes of the ' + monster.name + ' look vacant, as he starts to ' +
            'stumble around!', colors.light_green)


def cast_fireball():
    # ask the player for a target tile to throw a fireball at
    message('Left-click a target tile for the fireball, or right-click to ' +
            'cancel.', colors.light_cyan)

    (x, y) = target_tile()
    if x is None:
        message('Cancelled')
        return 'cancelled'
    message('The fireball explodes, burning everything within ' +
            str(FIREBALL_RADIUS) + ' tiles!', colors.orange)

    for obj in Game.area_map.entities:  # damage every fighter in range, including the player
        obj_fighter = obj.get_component(Fighter)
        if obj.distance(x, y) <= FIREBALL_RADIUS and obj_fighter:
            message('The ' + obj.name + ' gets burned for ' +
                    str(FIREBALL_DAMAGE) + ' hit points.', colors.orange)

            obj_fighter.take_damage(FIREBALL_DAMAGE)