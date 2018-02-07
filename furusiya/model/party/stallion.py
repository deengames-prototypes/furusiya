from model.gameobject import GameObject
import colors

class Stallion(GameObject):
    def __init__(self, player):
        super().__init__(0, 0, '=', 'stallion', color=colors.sepia, blocks=True,
        ai = StallionAi())

        self.player = player

class StallionAi:
    def take_turn(self):
        print("Stallion whinnies!")
