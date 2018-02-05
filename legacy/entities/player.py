from legacy.ecs.entity import Entity


class Player(Entity):
    # Singleton-ish
    INSTANCE = None

    def __init__(self):
        super().__init__('@', (255, 255, 255))
        Player.INSTANCE = self