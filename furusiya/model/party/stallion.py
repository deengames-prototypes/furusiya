import colors
from model.components.ai.stallion import StallionAi
from model.game_object import GameObject


class Stallion(GameObject):
    def __init__(self, player):
        super().__init__(0, 0, '=', 'stallion', color=colors.sepia, blocks=True)

        self.ai = StallionAi(self)
        self.original_ai = self.ai

        self.player = player
