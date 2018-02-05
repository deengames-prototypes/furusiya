from furusiya.components.walkers.random_walker import RandomWalker
from furusiya.ecs.entity import Entity
from furusiya.entities.player import Player
import math


class Monster(Entity):

    # Tuple of monster data needed to construct a monster
    ALL_MONSTERS = {
        "tiger": ('t', (255, 128, 0))
    }

    def __init__(self, character, colour, area_map):
        super().__init__(character, colour)
        self.set(RandomWalker(area_map, self))
        self.target = Player.INSTANCE

    def walk(self):
        distance_to_target = math.hypot(self.x - self.target.x, self.y - self.target.y)
        if distance_to_target == 1:
            # FIGHT!
            print("{} bites {}!".format(self, self.target))
        else:
            # TODO: stalk if the user is close
            self.get(RandomWalker).walk()
