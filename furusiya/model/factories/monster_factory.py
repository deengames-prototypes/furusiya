from model.components.ai.monster import BasicMonster

from death_functions import monster_death
from model.components.fighter import Fighter
from model.entities.monster import Monster


def create_monster(data, x, y, colour, name):
    monster = Monster(x, y, name[0], name, colour, blocks=True)

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

    monster.set_ai(BasicMonster(monster))

    return monster
