from game import Game
from model.components.ai.monster import BasicMonster

from model.helper_functions.death_functions import monster_death
from model.components.fighter import Fighter
from model.components.xp import XPComponent
from model.entities.game_object import GameObject


def create_monster(data, x, y, colour, name):
    monster = GameObject(x, y, name[0], name, colour, blocks=True)

    Game.fighter_system.set(
        monster, Fighter(
            owner=monster,
            hp=data.health,
            defense=data.defense,
            power=data.attack,
            death_function=monster_death,
            hostile=True
        )
    )

    Game.xp_system.set(
        monster, XPComponent(
            owner=monster,
            xp=data.xp
        )
    )

    Game.ai_system.set(monster, BasicMonster(monster))

    return monster
