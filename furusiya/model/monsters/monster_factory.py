from model.fighter import Fighter
from model.ai import BasicMonster
from model.gameobject import GameObject

def create_monster(data, x, y, colour, name, death_function):
    fighter_component = Fighter(hp=data.health, defense=data.defense,
        power=data.attack, xp=data.xp, death_function=death_function)

    ai_component = BasicMonster()

    monster = GameObject(x, y, name[0], name, colour, blocks=True, fighter=fighter_component, ai=ai_component)
    return monster