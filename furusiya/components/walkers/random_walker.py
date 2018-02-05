import random


class RandomWalker:
    """Walks randomly. Does this by mutating the parent entity's x/y coordinates."""
    def __init__(self, area_map, parent):
        self.area_map = area_map
        self.parent = parent

    def walk(self):
        valid_options = [0, 1, 2, 3]
        random.shuffle(valid_options)
        base_x, base_y = self.parent.x, self.parent.y

        while len(valid_options):
            (x, y) = (self.parent.x, self.parent.y)            
            n = valid_options.pop()

            if n == 0:
                x += 1
            elif n == 1:
                x -= 1
            elif n == 2:
                y += 1
            elif n == 3:
                y -= 1
            if self.area_map.is_on_map(x, y) and self.area_map.is_walkable(x, y):
                self.parent.x, self.parent.y = x, y
                return

        # Restore to original position
        self.parent.x, self.parent.y = base_x, base_y
        raise ValueError("There are no available adjacent locations")