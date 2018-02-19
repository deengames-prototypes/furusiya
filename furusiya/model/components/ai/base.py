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
        assert isinstance(other.num_turns, int), "The passed AI's num_turns attribute can only be an int."

        if type(other) == type(self):  # If they're the same AI type, extend this one
            if self.num_turns is not None:
                self.num_turns += other.num_turns
                return
            # Else, continue on setting it anyway

        Game.ai_system.set(self.owner, other)

        def temporary_take_turn():
            if other.num_turns > 0:
                other._take_turn()
            else:
                Game.ai_system.set(self.owner, self)
                self.take_turn()

        other.take_turn = temporary_take_turn
