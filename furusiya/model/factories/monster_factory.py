from model.components.ai.monster import BasicMonster

from death_functions import monster_death
from model.components.fighter import Fighter
from model.entities.game_object import GameObject
from model.systems.ai_system import AISystem


def create_monster(data, x, y, colour, name):
    monster = GameObject(x, y, name[0], name, colour, blocks=True, hostile=True)

    monster.set_component(
        Fighter(
            owner=monster,
            hp=data.health,
            defense=data.defense,
            power=data.attack,
            xp=data.xp,
            death_function=monster_death
        )
    )

    AISystem.set_ai(monster, BasicMonster(monster))

    return monster
