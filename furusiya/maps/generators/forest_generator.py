from furusiya.ecs.entity import Entity
from furusiya.entities.monster import Monster
from furusiya.components.walkers.random_walker import RandomWalker
import math
import random

# Generates a scary forest map in entirety, by mutating map tiles.
# Includes population of monsters, map items, etc.
class ForestGenerator:

    TREE_PERCENTAGE = 1/4 # This percent of the map area should be trees
    TREE_COPSE_SIZE = 5 # Create copses of N trees at a time
    NUM_MONSTERS = (5, 8) # min-max
    MONSTERS = ["tiger"]

    GROUND_CHARACTER = '.'
    GROUND_COLOUR = (64, 48, 0)

    TREE_CHARACTER = 'T'
    TREE_COLOURS = [(64, 128, 0),
                    (0, 64, 0)]

    def __init__(self, width, height, area_map):
        self._width = width
        self._height = height
        self._area_map = area_map
        self._generate_trees()
        self._generate_monsters()


    def _generate_trees(self):        
        for x in range(0, self._area_map.width):
            for y in range(0, self._area_map.height):
                self._convert_to_ground(self._area_map.tiles[x][y])

        total = math.floor(self._width * self._height * ForestGenerator.TREE_PERCENTAGE)
        
        # Creates little clusters of N trees
        while total > 0:
            to_create = min(ForestGenerator.TREE_COPSE_SIZE, total)
            self._random_walk(self._area_map.tiles, to_create)
            total -= to_create

        # It's too bad those little clusters sometimes create "holes" that are
        # unreachable on all sides. It would be a pity if the stairs ended up
        # spawning there.
        #
        # Since mining is not part of the core experience, let's flood-fill the
        # ground, and any non-flood-filled ground tiles can turn into trees.
        self._fill_ground_holes(self._area_map.tiles)


    """Breadth-first search. Assuming "position" is reachable,
    mark any other ground tiles that we can reach, as reachable."""
    def _breadth_first_search(self, map_tiles, start_position):    
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
                if x < self._width - 1 and map_tiles[x + 1][y].is_walkable and (x+1, y) not in queue and (x+1, y) not in explored:
                    queue.append((x+1, y))
                if y > 0 and map_tiles[x][y-1].is_walkable and (x, y-1) not in queue and (x, y-1) not in explored:
                    queue.append((x, y-1))
                if y < self._height - 1 and map_tiles[x][y+1].is_walkable and (x, y+1) not in queue and (x, y+1) not in explored:
                    queue.append((x, y+1))

        return explored


    def _fill_ground_holes(self, map_tiles):
        start_position = self._find_empty_ground(map_tiles)

        all_ground_tiles = [(x, y) for y in range (0, self._height)
            for x in range (0, self._width) if map_tiles[x][y].is_walkable]

        reachable = self._breadth_first_search(map_tiles, start_position)

        unreachable = [(x, y) for (x, y) in all_ground_tiles if (x, y) not in reachable]

        for (x, y) in unreachable:
            self._convert_to_tree(map_tiles[x][y])


    """Look for a 3x3 patch of ground. It's unlikely that this is contained
    within a copse of trees as an enclosed area. If we're wrong ... well.
    I suppose you can always exit and re-enter the dungeon if that happens."""
    def _find_empty_ground(self, map_tiles):
        for x in range(1, self._width - 1):
            for y in range(1, self._height - 1):
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
    def _random_walk(self, map_tiles, num_tiles):
        x = random.randint(0, self._width - 1)
        y = random.randint(0, self._height - 1)

        # This smells. We need a dummy entity.
        e = Entity(None, None)
        e.x, e.y = (x, y)
        walker = RandomWalker(self._area_map, e)

        while (num_tiles > 0):
            try:
                walker.walk()
                self._convert_to_tree(map_tiles[e.x][e.y])
                num_tiles -= 1
            except ValueError as no_walkable_adjacents_error:
                # While loop will not terminate, we'll try elsewhere
                # Randomly move, even if there's a tree there. 
                e.x += random.randint(-1, 1)
                e.y += random.randint(-1, 1)

    def _convert_to_ground(self, map_tile):
        map_tile.is_walkable = True
        map_tile.character = ForestGenerator.GROUND_CHARACTER
        map_tile.colour = ForestGenerator.GROUND_COLOUR


    def _convert_to_tree(self, map_tile):
        map_tile.is_walkable = False
        map_tile.character = ForestGenerator.TREE_CHARACTER
        map_tile.colour = random.choice(ForestGenerator.TREE_COLOURS)

    
    def _generate_monsters(self):
        min_monsters, max_monsters = ForestGenerator.NUM_MONSTERS
        num_monsters = random.randint(min_monsters, max_monsters)

        while num_monsters > 0:
            (x, y) = self._find_empty_tile()
            monster_name = random.choice(ForestGenerator.MONSTERS)

            data = Monster.ALL_MONSTERS[monster_name]
            m = Monster(data[0], data[1], self._area_map) # character/colour
            m.x = x
            m.y = y
            self._area_map.entities.append(m)
            num_monsters -= 1


    def _find_empty_tile(self):
        while True:
            x = random.randint(0, self._area_map.width - 1)
            y  = random.randint(0, self._area_map.height - 1)
            if self._area_map.tiles[x][y].is_walkable:
                break
        return (x, y)
        
