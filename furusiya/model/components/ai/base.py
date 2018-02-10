from model.components.base import Component
from model.systems.ai_system import AISystem


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

    def set_temporary(self, other):
        AISystem.set_ai(self.owner, other)

        def new_take_turn():
            if other.num_turns > 0:
                other._take_turn()
            else:
                AISystem.set_ai(self.owner, self)
                self.take_turn()

        other.take_turn = new_take_turn
