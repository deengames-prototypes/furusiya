from random import randint

import colors
import config
from constants import CONFUSE_NUM_TURNS
from main_interface import Game, message


class BasicMonster:
    """
    AI for a basic monster.
    """
    def take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if (monster.x, monster.y) in Game.visible_tiles:

            # move towards player if far away
            if monster.distance_to(Game.player) >= 2:
                monster.move_towards(Game.player.x, Game.player.y)

            # close enough, attack! (if the player is still alive.)
            elif Game.player.fighter.hp > 0:
                monster.fighter.attack(Game.player)


class StunnedMonster:
    """
    AI for a temporarily stunned monster (reverts to previous AI after a while).
    """
    def __init__(self, owner, num_turns=config.data.weapons.numTurnsStunned):
        self.num_turns = num_turns
        self.owner = owner

    def take_turn(self):
        if self.num_turns > 0:  # still stunned ...
            self.num_turns -= 1
            self.owner.char = str(self.num_turns)[0]  # last digit
        else:
            # restore the previous AI (this one will be deleted because it's not
            # referenced anymore)
            self.owner.ai = self.owner.original_ai
            message('The ' + self.owner.name + ' is no longer stunned!', colors.red)
            self.owner.char = self.owner.name[0]


class ConfusedMonster:
    """
    AI for a temporarily confused monster (reverts to previous AI after a while).
    """
    def __init__(self, num_turns=CONFUSE_NUM_TURNS):
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:  # still confused...
            # move in a random direction, and decrease the number of turns confused
            self.owner.move(randint(-1, 1), randint(-1, 1))
            self.num_turns -= 1

        else:
            # restore the previous AI (this one will be deleted because it's not
            # referenced anymore)
            self.owner.ai = self.original_ai
            message('The ' + self.owner.name + ' is no longer confused!', colors.red)