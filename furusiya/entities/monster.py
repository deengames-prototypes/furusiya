from furusiya.components.walkers.random_walker import RandomWalker
from furusiya.ecs.entity import Entity

class Monster(Entity):

    # Tuple of monster data needed to construct a monster
    ALL_MONSTERS = {
        "tiger": ('t', (255, 128, 0))
    }

    def __init__(self, character, colour, area_map):
        super().__init__(character, colour)
        self.components[RandomWalker] = RandomWalker(area_map, self)

    def walk(self):
        self.components.get(RandomWalker).walk()