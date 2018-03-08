from game import Game
from model.config import config


def can_use_skill(cost: int) -> bool:
    skill_component = Game.skill_system.get(Game.player)
    if skill_component.can_use_skill(cost):
        skill_component.use_skill(cost)
        return True
    else:
        return False


def can_use_horse_skill(cost: int) -> bool:
    if config.data.stallion.enabled:
        skill_component = Game.skill_system.get(Game.stallion)
        if skill_component.can_use_skill(cost) and Game.stallion.is_mounted:
            skill_component.use_skill(cost)
            return True

    return False
