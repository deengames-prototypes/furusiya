import random

from model.maps.map_tile import MapTile

class AreaMap:

    def __init__(self, width, height, walkable=False):
        self.tiles = []
        self.entities = []
        self.width = width
        self.height = height

        # Create a 2D structure of tiles
        for x in range(0, self.width):
            self.tiles.append([])
            for y in range(0, self.height):
                self.tiles[x].append(MapTile(walkable))

    def is_on_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_entities_on(self, x, y):
        return [
            e
            for e in self.entities
            if (e.x, e.y) == (x, y)
        ]

    def is_walkable(self, x, y):
        return (self.is_on_map(x, y)
                and self.tiles[x][y].is_walkable
                and len([
                            e
                            for e in self.get_entities_on(x, y)
                            if e.blocks
                        ]) == 0)

    def is_visible_tile(self, x, y):
        return self.is_on_map(x, y) and not self.tiles[x][y].block_sight

    def place_on_random_ground(self, entity):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)

        # If the tile is a tree or occupied, pick a different one
        while not self.is_walkable(x, y):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

        entity.x = x
        entity.y = y
        self.entities.append(entity)
    
def filter_tiles(tiles, filter_callback):
    return [
        (x, y)
        for x, y in tiles
        if filter_callback(x, y)
    ]
