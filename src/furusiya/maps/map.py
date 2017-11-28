import random

class Map:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        self.entities = []

        # Create a 2D structure of tiles
        for x in range(0, self.width):
            self.tiles.append([])
            for y in range(0, self.height):
                self.tiles[x].append(MapTile())

    def place_on_random_ground(self, entity):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)

        # If the tile is a tree or occupied, pick a different one
        while self.tiles[x][y].is_walkable == False or [e for e in self.entities if e.x == x and e.y == y]:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

        entity.x = x
        entity.y = y
        self.entities.append(entity)

class MapTile:
    def __init__(self):
        self.is_walkable = True
        self.character = '.'
        self.colour = (128, 128, 128)