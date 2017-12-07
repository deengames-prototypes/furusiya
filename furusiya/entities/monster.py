from furusiya.ecs.entity import Entity

class Monster(Entity):

    # Tuple of monster data needed to construct a monster
    ALL_MONSTERS = {
        "tiger": ('t', (255, 128, 0))
    }

    def __init__(self, character, colour):
        super().__init__(character, colour)