from furusiya.ecs.entity import Entity

class Player(Entity):
    def __init__(self):
        super().__init__('@', (255, 255, 255))