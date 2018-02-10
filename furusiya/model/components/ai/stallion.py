from model.components.ai.base import AbstractAI


class StallionAi(AbstractAI):
    def _take_turn(self):
        print("Stallion whinnies!")
