from random import randint

import colors
from model.config import config
from main_interface import message
from model.components.ai.monster import StunnedMonster
from model.systems.ai_system import AISystem


class Sword:
    """
    A sword. It sometimes incapacitates (stuns) the opponent due to damage
    inflicted. As a class, it doesn't calculate or deal damage; merely adds
    effects on top of the combat algorithms. (This is true of all weapons.)
    """
    def __init__(self, owner):
        self.owner = owner

    def attack(self, target):
        if config.data.features.swordStuns and AISystem.has_ai(target):
            if randint(0, 100) <= config.data.weapons.swordStunProbability:
                target_ai = AISystem.get_ai(target)
                if config.data.features.stunsStack:
                    if isinstance(target_ai, StunnedMonster):
                        # Stack the stun
                        target_ai.num_turns += config.data.weapons.numTurnsStunned
                    else:
                        target_ai.temporarily_switch_to(StunnedMonster(target))
                else:
                    # Copy-pasta from two lines above
                    target_ai.temporarily_switch_to(StunnedMonster(target))
                message('{} looks incapacitated!'.format(target.name), colors.light_green)