from model.components.ai.monster import BasicMonster

from model.helper_functions.death_functions import monster_death
from model.components.fighter import Fighter
from model.components.xp import XPComponent
from model.entities.game_object import GameObject
from model.systems.ai_system import AISystem
from model.systems.fighter_system import FighterSystem
from model.systems.xp_system import XPSystem


def create_monster(data, x, y, colour, name):
    monster = GameObject(x, y, name[0], name, colour, blocks=True, hostile=True)

    FighterSystem.set_fighter(
        monster, Fighter(
            owner=monster,
            hp=data.health,
            defense=data.defense,
            power=data.attack,
            death_function=monster_death
        )
    )

    XPSystem.set_experience(
        monster, XPComponent(
            owner=monster,
            xp=data.xp
        )
    )

    AISystem.set_ai(monster, BasicMonster(monster))

    return monster
