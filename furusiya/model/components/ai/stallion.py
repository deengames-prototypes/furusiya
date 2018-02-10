from model.components.ai.base import AI


class StallionAi(AI):
    def _take_turn(self):
        print("Stallion whinnies!")
