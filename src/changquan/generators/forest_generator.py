from random import randint
import random

# TODO: Convert into a REAL generator, not a mutator of sorts.
# TODO: Figure out the best approximation of private methods in Python3
class ForestGenerator:

    TREE_PERCENTAGE = 1/6 # This percent of the map area should be trees
    TREE_COPSE_SIZE = 10 # Create copses of N trees at a time

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate_trees(self):
        data = [] # true if solid
        for x in range(0, self.width):
            data.append([])
            for y in range(0, self.height):
                data[x].append(False) # walkable
                
        total = self.width * self.height * ForestGenerator.TREE_PERCENTAGE
        
        # Creates little clusters of N trees
        while total > 0:
            to_create = min(ForestGenerator.TREE_COPSE_SIZE, total)
            self.__random_walk(data, to_create)
            total -= to_create

        # It's too bad those little clusters sometimes create "holes" that are
        # unreachable on all sides. It would be a pity if the stairs ended up
        # spawning there.
        #
        # Since mining is not part of the core experience, let's flood-fill the
        # ground, and any non-flood-filled ground tiles can turn into trees.
        self.__fill_ground_holes(data)

        return data

    def __breadth_first_search(self, data, start_position):
        # Breadth-first search. Assuming "position" is reachable,
        # mark any other ground tiles that we can reach, as reachable.
        explored = []
        queue = [start_position]

        while queue:
            position = queue.pop()
            (x, y) = position
            if data[x][y] == False: # ground tile
                explored.append(position)
                # Check each adjacent tile. If it's on-map, walkable, and not queued/explored,
                # then it's a candidate for an unwalkable tile.
                if x > 0 and data[x-1][y] == False and (x-1, y) not in queue and (x-1, y) not in explored:
                    queue.append((x-1, y))
                if x < self.width - 1 and data[x + 1][y] == False and (x+1, y) not in queue and (x+1, y) not in explored:
                    queue.append((x+1, y))
                if y > 0 and data[x][y-1] == False and (x, y-1) not in queue and (x, y-1) not in explored:
                    queue.append((x, y-1))
                if y < self.height - 1 and data[x][y+1] == False and (x, y+1) not in queue and (x, y+1) not in explored:
                    queue.append((x, y+1))

        return explored

    def __fill_ground_holes(self, data):
        start_position = self.__find_empty_ground(data)
        
        all_ground_tiles = [(x, y) for y in range (0, self.height)
            for x in range (0, self.width) if data[x][y] == False]
        
        reachable = self.__breadth_first_search(data, start_position)

        unreachable = [(x, y) for (x, y) in all_ground_tiles if (x, y) not in reachable]

        for (x, y) in unreachable:
            data[x][y] = 'X' # make it a tree


    def __find_empty_ground(self, data):
        # Look for a 3x3 patch of ground. It's unlikely that this is contained
        # within a copse of trees as an enclosed area. If we're wrong ... well.
        # I suppose you can always exit and re-enter the dungeon if that happens.
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if data[x][y] == False and data[x - 1][y] == False and \
                data[x + 1][y] == False and data[x][y - 1] == False and \
                data[x][y + 1] == False and \
                data[x - 1][y - 1] == False and data[x + 1][y - 1] == False and \
                data[x - 1][y + 1] == False and data[x + 1][y + 1] == False:
                    return (x, y)

        raise Exception("Can't find any empty ground with empty adjacent tiles!")

    def __random_walk(self, data, num_tiles):
        # Pick a random point, walk to a random adjacent point.
        # If it's a floor tile, make it a wall tile, and decrement
        # the number of tiles we have to walk.
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

            if x >= 0 and x < self.width and y >= 0 and y < self.height and data[x][y] == False: # walkable
                data[x][y] = True # tree
                num_tiles -= 1

            # Stay in bounds.
            if x < 0 or x >= self.width:
                x = randint(0, self.width - 1)
            
            if y < 0 or y >= self.height:
                y = randint(0, self.height - 1)