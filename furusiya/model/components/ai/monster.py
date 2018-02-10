from random import randint

import colors
from model.config import config
from constants import CONFUSE_NUM_TURNS
from main_interface import Game, message
from model.components.ai.base import AI
from model.components.fighter import Fighter


class BasicMonster(AI):
    """
    AI for a basic monster.
    """
    def _take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if (monster.x, monster.y) in Game.renderer.visible_tiles:

            # move towards player if far away
            if monster.distance_to(Game.player) >= 2:
                monster.move_towards(Game.player.x, Game.player.y)

            # close enough, attack! (if the player is still alive.)
            elif Game.player.get_component(Fighter).hp > 0:
                monster.get_component(Fighter).attack(Game.player)


class StunnedMonster(AI):
    """
    AI for a temporarily stunned monster (reverts to previous AI after a while).
    """
    def __init__(self, owner, num_turns=None):
        super().__init__(owner, num_turns or config.data.weapons.numTurnsStunned)

    def _take_turn(self):
        if self.num_turns > 0:  # still stunned ...
            self.num_turns -= 1
            self.owner.char = str(self.num_turns)[0]  # last digit

        if self.num_turns == 0:
            message('The ' + self.owner.name + ' is no longer stunned!', colors.red)
            self.owner.char = self.owner.name[0]


class ConfusedMonster(AI):
    """
    AI for a temporarily confused monster (reverts to previous AI after a while).
    """
    def __init__(self, owner, num_turns=None):
        super().__init__(owner, num_turns or CONFUSE_NUM_TURNS)

    def _take_turn(self):
        if self.num_turns > 0:  # still confused...
            # move in a random direction, and decrease the number of turns confused
            self.owner.move(randint(-1, 1), randint(-1, 1))
            self.num_turns -= 1

        if self.num_turns == 0:
            message('The ' + self.owner.name + ' is no longer confused!', colors.red)
