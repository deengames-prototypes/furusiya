from model.components.ai.base import AbstractAI


class StallionAi(AbstractAI):
    def _take_turn(self):
        if self.owner.distance_to(self.owner.player) >= 2:
            self.owner.move_towards(self.owner.player.x, self.owner.player.y)
