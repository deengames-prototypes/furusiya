import colors
from model.components.ai.stallion import StallionAi
from model.entities.game_object import GameObject
from model.systems.ai_system import AISystem


class Stallion(GameObject):
    def __init__(self, player):
        super().__init__(0, 0, '=', 'stallion', color=colors.sepia, blocks=True)

        AISystem.set_ai(self, StallionAi(self))
        self.player = player
