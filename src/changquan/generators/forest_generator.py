from random import randint
import random

class ForestGenerator:
    DELETE_PERCENTAGE = 0.5

    def __init__(self, width, height, is_walkable = True):
        self.width = width
        self.height = height
        self.data = []
        for x in range(0, width):
            self.data.append([])
            for y in range(0, height):
                self.data[x].append(is_walkable) # walkable

    def random_walk(self, num_tiles, is_walkable = False):
        # Pick a random point, walk to a random adjacent point.
        # If wall, make it floor, and decrement num_tiles.
        # Repeat until num_tiles is 0
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)

        while (num_tiles > 0):
            n = random.randrange(0, 4)
            if n == 0:
                x += 1
            elif n == 1:
                x -= 1
            elif n == 2:
                y += 1
            elif n == 3:
                y -= 1
            else:
                raise "Invalid state!"

            if x >= 0 and x < self.width and y >= 0 and y < self.height and self.data[x][y] == (not is_walkable): # solid
                self.data[x][y] = is_walkable
                num_tiles -= 1

            # Stay in bounds.
            if x < 0 or x >= self.width:
                x = randint(0, self.width - 1)
            
            if y < 0 or y >= self.height:
                y = randint(0, self.height - 1)