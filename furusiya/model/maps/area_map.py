import random


class AreaMap:

    # TODO: these should be the renderer's concern, not the map's.
    DARK_GROUND_COLOUR = (32, 32, 32)
    DARK_WALL_COLOUR = (48, 48, 48)
    LIGHT_GROUND_COLOUR = (128, 128, 128)
    LIGHT_WALL_COLOUR = (192, 192, 192)
    GROUND_CHARACTER = '.'
    WALL_CHARACTER = '#'

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


# TODO: extract into its own file
class MapTile:
    def __init__(self, walkable=False):
        self.is_explored = False
        self.convert_to_ground()

    def convert_to_wall(self, character=AreaMap.WALL_CHARACTER, colour=AreaMap.LIGHT_WALL_COLOUR, dark_colour=AreaMap.DARK_WALL_COLOUR):
        self.is_walkable = False
        self.block_sight = True
        self._set_character_and_colour(character, colour, dark_colour)
        
    def convert_to_ground(self, character=AreaMap.GROUND_CHARACTER, colour=AreaMap.LIGHT_GROUND_COLOUR, dark_colour=AreaMap.DARK_GROUND_COLOUR):
        self.is_walkable = True
        self.block_sight = False
        self._set_character_and_colour(character, colour, dark_colour)
        
    def _set_character_and_colour(self, character, colour, dark_colour):
        self.character = character
        self.colour = colour
        self.dark_colour = dark_colour