from model.components.ai.monster import BasicMonster

from death_functions import monster_death
from model.components.fighter import Fighter
from model.game_object import GameObject


def create_monster(data, x, y, colour, name):
    fighter_component = Fighter(hp=data.health, defense=data.defense,
                                power=data.attack, xp=data.xp, death_function=monster_death)

    monster = GameObject(x, y, name[0], name, colour, blocks=True,
                         fighter=fighter_component)

    ai = BasicMonster(monster)
    monster.ai = ai
    monster.original_ai = ai

    return monster
