from furusiya.entities.monster import Monster
import math
import random

# Generates a scary forest map in entirety, by mutating map tiles.
# Includes population of monsters, map items, etc.
class ForestGenerator:

    TREE_PERCENTAGE = 1/6 # This percent of the map area should be trees
    TREE_COPSE_SIZE = 10 # Create copses of N trees at a time
    NUM_MONSTERS = (5, 8) # min-max
    MONSTERS = ["tiger"]

    GROUND_CHARACTER = '.'
    GROUND_COLOUR = (64, 48, 0)

    TREE_CHARACTER = 'T'
    TREE_COLOURS = [(64, 128, 0),
                    (0, 64, 0)]

    def __init__(self, width, height):
        self.width = width
        self.height = height


    def generate(self, map):
        self.__generate_trees(map)
        self.__generate_monsters(map)

    def __generate_trees(self, map):        
        for x in range(0, map.width):
            for y in range(0, map.height):
                self.__convert_to_ground(map.tiles[x][y])

        total = math.floor(self.width * self.height * ForestGenerator.TREE_PERCENTAGE)
        
        # Creates little clusters of N trees
        while total > 0:
            to_create = min(ForestGenerator.TREE_COPSE_SIZE, total)
            self.__random_walk(map.tiles, to_create)
            total -= to_create

        # It's too bad those little clusters sometimes create "holes" that are
        # unreachable on all sides. It would be a pity if the stairs ended up
        # spawning there.
        #
        # Since mining is not part of the core experience, let's flood-fill the
        # ground, and any non-flood-filled ground tiles can turn into trees.
        self.__fill_ground_holes(map.tiles)


    """Breadth-first search. Assuming "position" is reachable,
    mark any other ground tiles that we can reach, as reachable."""
    def __breadth_first_search(self, map_tiles, start_position):    
        explored = []
        queue = [start_position]

        while queue:
            position = queue.pop()
            (x, y) = position
            if map_tiles[x][y].is_walkable: # ground tile
                explored.append(position)
                # Check each adjacent tile. If it's on-map, walkable, and not queued/explored,
                # then it's a candidate for an unwalkable tile.
                if x > 0 and map_tiles[x-1][y].is_walkable and (x-1, y) not in queue and (x-1, y) not in explored:
                    queue.append((x-1, y))
                if x < self.width - 1 and map_tiles[x + 1][y].is_walkable and (x+1, y) not in queue and (x+1, y) not in explored:
                    queue.append((x+1, y))
                if y > 0 and map_tiles[x][y-1].is_walkable and (x, y-1) not in queue and (x, y-1) not in explored:
                    queue.append((x, y-1))
                if y < self.height - 1 and map_tiles[x][y+1].is_walkable and (x, y+1) not in queue and (x, y+1) not in explored:
                    queue.append((x, y+1))

        return explored


    def __fill_ground_holes(self, map_tiles):
        start_position = self.__find_empty_ground(map_tiles)

        all_ground_tiles = [(x, y) for y in range (0, self.height)
            for x in range (0, self.width) if map_tiles[x][y].is_walkable]

        reachable = self.__breadth_first_search(map_tiles, start_position)

        unreachable = [(x, y) for (x, y) in all_ground_tiles if (x, y) not in reachable]

        for (x, y) in unreachable:
            self.__convert_to_tree(map_tiles[x][y])


    """Look for a 3x3 patch of ground. It's unlikely that this is contained
    within a copse of trees as an enclosed area. If we're wrong ... well.
    I suppose you can always exit and re-enter the dungeon if that happens."""
    def __find_empty_ground(self, map_tiles):
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if map_tiles[x][y].is_walkable and map_tiles[x - 1][y].is_walkable and \
                map_tiles[x + 1][y].is_walkable and map_tiles[x][y - 1].is_walkable and \
                map_tiles[x][y + 1].is_walkable and \
                map_tiles[x - 1][y - 1].is_walkable and map_tiles[x + 1][y - 1].is_walkable and \
                map_tiles[x - 1][y + 1].is_walkable and map_tiles[x + 1][y + 1].is_walkable:
                    return (x, y)

        raise Exception("Can't find any empty ground with empty adjacent tiles!")


    """Pick a random point, walk to a random adjacent point.
    If it's a floor tile, make it a wall tile, and decrement
    the number of tiles we have to walk.
    Repeat until num_tiles is 0"""
    def __random_walk(self, map_tiles, num_tiles):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)

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

            if x >= 0 and x < self.width and y >= 0 and y < self.height and map_tiles[x][y].is_walkable:
                self.__convert_to_tree(map_tiles[x][y])
                num_tiles -= 1

            # Stay in bounds.
            if x < 0 or x >= self.width:
                x = random.randint(0, self.width - 1)
            
            if y < 0 or y >= self.height:
                y = random.randint(0, self.height - 1)


    def __convert_to_ground(self, map_tile):
        map_tile.is_walkable = True
        map_tile.character = ForestGenerator.GROUND_CHARACTER
        map_tile.colour = ForestGenerator.GROUND_COLOUR


    def __convert_to_tree(self, map_tile):
        map_tile.is_walkable = False
        map_tile.character = ForestGenerator.TREE_CHARACTER
        map_tile.colour = random.choice(ForestGenerator.TREE_COLOURS)

    
    def __generate_monsters(self, map):
        min_monsters, max_monsters = ForestGenerator.NUM_MONSTERS
        num_monsters = random.randint(min_monsters, max_monsters)

        while num_monsters > 0:
            (x, y) = self.__find_empty_tile(map)
            monster_name = random.choice(ForestGenerator.MONSTERS)

            data = Monster.ALL_MONSTERS[monster_name]
            m = Monster(data[0], data[1]) # character/colour
            m.x = x
            m.y = y
            map.entities.append(m)
            print("Generated a tiger at {}, {}".format(m.x, m.y))
            num_monsters -= 1

    def __find_empty_tile(self, map):
        while True:
            x = random.randint(0, map.width - 1)
            y  = random.randint(0, map.height - 1)
            if map.tiles[x][y].is_walkable:
                break
        return (x, y)
        
