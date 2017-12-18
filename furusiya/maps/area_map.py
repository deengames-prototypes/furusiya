import random

class AreaMap:
    
    def __init__(self, width, height):
        self.tiles = []
        self.entities = []
        self._width = width
        self._height = height

        # Create a 2D structure of tiles
        for x in range(0, self._width):
            self.tiles.append([])
            for y in range(0, self._height):
                self.tiles[x].append(MapTile())

    def is_on_map(self, x, y):
        return x >= 0 and x < self._width and y >= 0 and y < self._height


    def is_walkable(self, x, y):
        return x >= 0 and x < self._width and y >= 0 and y < self._height and \
        self.tiles[x][y].is_walkable and \
        len([e for e in self.entities if e.x == x and e.y == y]) == 0


    def place_on_random_ground(self, entity):
        x = random.randint(0, self._width)
        y = random.randint(0, self._height)

        # If the tile is a tree or occupied, pick a different one
        while not self.is_walkable(x, y):
            x = random.randint(0, self._width)
            y = random.randint(0, self._height)

        entity.x = x
        entity.y = y
        self.entities.append(entity) 

    @property

    def width(self):
        return self._width


    @property
    def height(self):
        return self._height

class MapTile:
    def __init__(self):
        self.is_walkable = True
        self.character = '.'
        self.colour = (128, 128, 128)
        self.is_explored = False