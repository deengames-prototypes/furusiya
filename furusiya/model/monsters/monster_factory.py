from model.fighter import Fighter
from model.ai.monster import BasicMonster
from model.game_object import GameObject
from death_functions import monster_death


def create_monster(data, x, y, colour, name):
    fighter_component = Fighter(hp=data.health, defense=data.defense,
                                power=data.attack, xp=data.xp, death_function=monster_death)

    monster = GameObject(x, y, name[0], name, colour, blocks=True,
                         fighter=fighter_component)

    ai = BasicMonster(monster)
    monster.ai = ai
    monster.original_ai = ai

    return monster
