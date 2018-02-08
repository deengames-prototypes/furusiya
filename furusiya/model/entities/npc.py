from model.components.ai.base import AI
from model.entities.game_object import GameObject


class NPC(GameObject):
    """
    Basic class representing a GameObject capable of smartly dealing with AIs

    As the name suggests, it is used for every NPC(monsters, stallion, otherwise)
    """
    def __init__(self, x, y, char, name, color, blocks=False):
        super().__init__(x, y, char, name, color, blocks)
        self.original_ai = None

    def _get_ai_components(self):
        return [
            k
            for k in self._components.keys()
            if issubclass(k, AI)
        ]

    @property
    def ai(self):
        ls = self._get_ai_components()
        return self.get_component(ls[0]) if len(ls) > 0 else None

    @ai.setter
    def ai(self, value):
        if not self.original_ai:
            self.original_ai = value

        ai_ls = self._get_ai_components()
        for k in ai_ls:
            self.remove_component(k)

        self.set_component(value)

    @ai.deleter
    def ai(self):
        ls = self._get_ai_components()
        self.remove_component(ls[0]) if len(ls) > 0 else None
