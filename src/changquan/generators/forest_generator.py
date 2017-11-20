from random import randint
import random

class ForestGenerator:
    DELETE_PERCENTAGE = 0.5
    TREE_BATCH_SIZE = 10
    TREE_PERCENTAGE = 1/6

    def __init__(self, width, height):
        # Hard-coded random seed for easier debugging
        # random.seed(1)
        
        self.width = width
        self.height = height
        self.data = [] # true if solid
        for x in range(0, width):
            self.data.append([])
            for y in range(0, height):
                self.data[x].append(False) # walkable

        self.generate_trees()

    def generate_trees(self):
        total = self.width * self.height * ForestGenerator.TREE_PERCENTAGE
        
        # Creates little clusters of N trees
        while total > 0:
            batch = min(ForestGenerator.TREE_BATCH_SIZE, total)
            total -= batch
            self.random_walk(batch)

        # It's too bad those little clusters sometimes create "holes" that are
        # unreachable on all sides. It would be a pity if the stairs ended up
        # spawning there.
        #
        # Since mining is not part of the core experience, let's flood-fill the
        # ground, and any non-flood-filled ground tiles can turn into trees.
        self.fill_ground_holes()

    def fill_ground_holes(self):
        position = self.find_empty_ground()
        queue = [position]
        
        # Add every ground tile to "unreachable"
        unreachable = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.data[x][y] == False: # walkable
                    coordinates = (x, y)
                    unreachable.append(coordinates)

        # Breadth-first search. Assuming "position" is reachable (empty 3x3),
        # mark any other ground tiles that we can reach, as reachable.
        explored = []

        while queue:
            position = queue.pop()
            (x, y) = position
            if self.data[x][y] == False: # ground tile
                #print("Removing {0}; ex={1}".format(position, explored))
                unreachable.remove(position)
                explored.append(position)
                # Check each adjacent tile. If it's on-map, walkable, and not queued/explored,
                # then it's a candidate for an unwalkable tile.
                if x > 0 and self.data[x-1][y] == False and (x-1, y) not in queue and (x-1, y) not in explored:
                    queue.append((x-1, y))
                if x < self.width - 1 and self.data[x + 1][y] == False and (x+1, y) not in queue and (x+1, y) not in explored:
                    queue.append((x+1, y))
                if y > 0 and self.data[x][y-1] == False and (x, y-1) not in queue and (x, y-1) not in explored:
                    queue.append((x, y-1))
                if y < self.height - 1 and self.data[x][y+1] == False and (x, y+1) not in queue and (x, y+1) not in explored:
                    queue.append((x, y+1))

        print("Done walking and found {0} unreachable tiles: {1}".format(len(unreachable), unreachable))
        while unreachable:
            (x, y) = unreachable.pop()
            self.data[x][y] = True # make it a tree

    # private
    def find_empty_ground(self):
        # Look for a 3x3 patch of ground. It's unlikely that this is contained
        # within a copse of trees as an enclosed area. If we're wrong ... well.
        # I suppose you can always exit and re-enter the dungeon if that happens.
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if self.data[x][y] == False and self.data[x - 1][y] == False and \
                self.data[x + 1][y] == False and self.data[x][y - 1] == False and \
                self.data[x][y + 1] == False and \
                self.data[x - 1][y - 1] == False and self.data[x + 1][y - 1] == False and \
                self.data[x - 1][y + 1] == False and self.data[x + 1][y + 1] == False:
                    return (x, y)

        raise Exception("Can't find any empty ground with empty adjacent tiles!")

    # private
    def random_walk(self, num_tiles):
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

            if x >= 0 and x < self.width and y >= 0 and y < self.height and self.data[x][y] == False: # walkable
                self.data[x][y] = True # tree
                num_tiles -= 1

            # Stay in bounds.
            if x < 0 or x >= self.width:
                x = randint(0, self.width - 1)
            
            if y < 0 or y >= self.height:
                y = randint(0, self.height - 1)