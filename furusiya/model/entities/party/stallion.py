import colors
from model.components.ai.stallion import StallionAi
from model.entities.npc import NPC


class Stallion(NPC):
    def __init__(self, player):
        super().__init__(0, 0, '=', 'stallion', color=colors.sepia, blocks=True)

        self.ai = StallionAi(self)
        self.player = player
