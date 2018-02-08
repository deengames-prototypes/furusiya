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

    def set_ai(self, ai):
        if not self.original_ai:
            self.original_ai = ai

        ai_ls = self._get_components_of_type(AI)
        for k in ai_ls:
            self.remove_component(k)

        self.set_component(ai)