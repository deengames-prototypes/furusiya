from model.components.base import Component


class AI(Component):
    """
    Base class for all AI components.
    This is what you'll want to pass to a GameObject's get_component method.
    """
    def take_turn(self):
        raise NotImplementedError()
