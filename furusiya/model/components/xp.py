from main_interface import message
from model.components.base import Component
from model.config import config
from model.systems.fighter_system import FighterSystem


class XP(Component):
    def __init__(self, owner, level=1, xp=0):
        super().__init__(owner)
        self.level = level
        self.xp = xp
        self.stats_points = 0

    def _xp_next_level(self):
        return 2 ** (self.level + 1) * config.data.player.expRequiredBase

    def gain_xp(self, amount):
        self.xp += amount
        # XP doubles every level. 40, 80, 160, ...
        # First level = after four orcs. Yeah, low standards.
        # DRY ya'ne
        while self.xp >= self._xp_next_level():
            self.level += 1
            self.stats_points += config.data.player.statsPointsOnLevelUp
            message(f"{self.owner.name.capitalize()} is now level {self.level}!")
            fighter = FighterSystem.get_fighter(self.owner)
            fighter.heal(fighter.max_hp)
