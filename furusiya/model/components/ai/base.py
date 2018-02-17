from game import Game
from model.components.base import Component


class AbstractAI(Component):
    """
    Base class for all AI components.
    """
    def __init__(self, owner, num_turns=None):
        super().__init__(owner)
        self.num_turns = num_turns
        self.take_turn = self._take_turn

    def _take_turn(self):
        raise NotImplementedError()

    def temporarily_switch_to(self, other):
        Game.ai_sys.set(self.owner, other)

        def temporary_take_turn():
            if other.num_turns > 0:
                other._take_turn()
            else:
                Game.ai_sys.set(self.owner, self)
                self.take_turn()

        other.take_turn = temporary_take_turn
