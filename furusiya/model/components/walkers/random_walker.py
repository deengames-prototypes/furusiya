import random


class RandomWalker:
    """Walks randomly. Does this by mutating the parent entity's x/y coordinates."""
    def __init__(self, area_map, parent):
        self.area_map = area_map
        self.parent = parent

    def walk(self):
        # Not ideal, but better than what was here previously.
        adjacent_tiles = [
            (self.parent.x + x_offset, self.parent.y + y_offset)
            for x_offset, y_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        ]
        random.shuffle(adjacent_tiles)

        for tile_x, tile_y in adjacent_tiles:
            if self.area_map.is_walkable(tile_x, tile_y):
                self.parent.x, self.parent.y = tile_x, tile_y
                return

        # if no free adjacent tiles, silently ignore
