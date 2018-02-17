import random

from model.maps.map_tile import MapTile
from model.rect import Rect


class AreaMap:
    def __init__(self, width, height):
        self.tiles = []
        self.entities = []
        self.width = width
        self.height = height

        # Create a 2D structure of tiles
        for x in range(0, self.width):
            self.tiles.append([])
            for y in range(0, self.height):
                self.tiles[x].append(MapTile())

    def is_on_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_entities_on(self, x, y):
        return [
            e
            for e in self.entities
            if (e.x, e.y) == (x, y)
        ]

    def get_entity_with_id(self, entity_id):
        for entity in self.entities:
            if entity.id == entity_id:
                return entity

        return None

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

        return self.entities.index(entity)

    def get_walkable_tile_within(self, rect):
        for tile_x in range(rect.x1, rect.x2):
            for tile_y in range(rect.y1, rect.y2):
                if self.is_walkable(tile_x, tile_y):
                    return tile_x, tile_y

        return None

    def get_walkable_tile_around(self, x, y, range_num):
        """
        returns a walkable tile in given range "around" x, y.
        tries to return closest tile there is.
        """
        already_processed = set()

        for delta in range(range_num):
            for width_range in range(-delta, delta):
                for height_range in range(-delta, delta):
                    if (width_range, height_range) not in already_processed:
                        already_processed.add((width_range, height_range))
                        rect = Rect(x, y, width_range, height_range)
                        tile = self.get_walkable_tile_within(rect)
                        if tile is not None:
                            return tile

        return None

    def place_around(self, entity, x, y):
        tile = self.get_walkable_tile_around(x, y, min(self.width, self.height))

        entity.x = tile[0]
        entity.y = tile[1]
        self.entities.append(entity)

        return self.entities.index(entity)

    def get_blocking_object_at(self, x, y):
        for obj in self.entities:
            if obj.blocks and (obj.x, obj.y) == (x, y):
                return obj

        return None


def filter_tiles(tiles, filter_callback):
    return [
        (x, y)
        for x, y in tiles
        if filter_callback(x, y)
    ]
