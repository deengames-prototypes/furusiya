from attrdict import AttrDict

import colors
import config
from constants import MAX_ROOMS, ROOM_MAX_SIZE, ROOM_MIN_SIZE, MAX_ROOM_MONSTERS, MAX_ROOM_ITEMS
from model.components.walkers.random_walker import RandomWalker
import math
from random import randint, choice

from model.item_callbacks import cast_heal, cast_lightning, cast_fireball, cast_confuse
from model.rect import Rect
from model.factories import monster_factory, item_factory


class ForestGenerator:
    """
    Generates a scary forest map in entirety, by mutating map tiles.
    Includes population of monsters, map items, etc.
    """
    TREE_PERCENTAGE = 1 / 4  # This percent of the map area should be trees
    TREE_COPSE_SIZE = 5  # Create copses of N trees at a time
    NUM_MONSTERS = (5, 8)  # min-max
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
        self._generate_objects()

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

    def _breadth_first_search(self, map_tiles, start_position):
        """
        Breadth-first search. Assuming "position" is reachable,
        mark any other ground tiles that we can reach, as reachable.
        """
        explored = []
        queue = [start_position]

        while queue:
            position = queue.pop()
            (x, y) = position
            if map_tiles[x][y].is_walkable:  # ground tile
                explored.append(position)
                # Check each adjacent tile. If it's on-map, walkable, and not queued/explored,
                # then it's a candidate for an unwalkable tile.

                def append_if_eligible(to_append):
                    tile = map_tiles[to_append[0]][to_append[1]]
                    if tile.is_walkable and to_append not in queue + explored:
                        queue.append(to_append)

                if x > 0:
                    append_if_eligible((x - 1, y))
                if x < self._width - 1:
                    append_if_eligible((x + 1, y))
                if y > 0:
                    append_if_eligible((x, y - 1))
                if y < self._height - 1:
                    append_if_eligible((x, y + 1))

        return explored

    def _fill_ground_holes(self, map_tiles):
        start_position = self._find_empty_ground(map_tiles)

        all_ground_tiles = [
            (x, y)
            for y in range(0, self._height)
            for x in range(0, self._width)
            if map_tiles[x][y].is_walkable
        ]

        reachable = self._breadth_first_search(map_tiles, start_position)

        unreachable = [(x, y) for (x, y) in all_ground_tiles if (x, y) not in reachable]

        for (x, y) in unreachable:
            self._convert_to_tree(map_tiles[x][y])

    def _find_empty_ground(self, map_tiles):
        """
        Look for a 3x3 patch of ground. It's unlikely that this is contained
        within a copse of trees as an enclosed area. If we're wrong ... well.
        I suppose you can always exit and re-enter the dungeon if that happens.
        """
        def is_empty_3x3(x, y):
            cond = True
            for x_ in range(x - 1, x + 2):
                for y_ in range(y - 1, y + 2):
                    cond = cond and map_tiles[x_][y_].is_walkable
            return cond

        for x in range(1, self._width - 1):
            for y in range(1, self._height - 1):
                if is_empty_3x3(x, y):
                    return x, y

        raise Exception("Can't find any empty ground with empty adjacent tiles!")

    def _random_walk(self, map_tiles, num_tiles):
        """
        Pick a random point, walk to a random adjacent point.
        If it's a floor tile, make it a wall tile, and decrement
        the number of tiles we have to walk.
        Repeat until num_tiles is 0
        """
        e = AttrDict({'x': (randint(0, self._width - 1)), 'y': (randint(0, self._height - 1))})
        walker = RandomWalker(self._area_map, e)

        while num_tiles > 0:
            try:
                walker.walk()
                self._convert_to_tree(map_tiles[e.x][e.y])
                num_tiles -= 1
            except ValueError as no_walkable_adjacents_error:
                # While loop will not terminate, we'll try elsewhere
                # Randomly move, even if there's a tree there.
                dx = randint(-1, 1)
                dy = randint(-1, 1) if dx == 0 else 0

                e.x += dx
                e.y += dy

    def _convert_to_ground(self, map_tile):
        map_tile.is_walkable = True
        map_tile.block_sight = False
        map_tile.character = ForestGenerator.GROUND_CHARACTER
        map_tile.colour = ForestGenerator.GROUND_COLOUR

    def _convert_to_tree(self, map_tile):
        map_tile.is_walkable = False
        map_tile.block_sight = True
        map_tile.character = ForestGenerator.TREE_CHARACTER
        map_tile.colour = choice(ForestGenerator.TREE_COLOURS)

    def _generate_objects(self):
        target = randint(MAX_ROOMS // 2, MAX_ROOMS)
        while target:
            x = randint(0, self._area_map.width - ROOM_MAX_SIZE)
            y = randint(0, self._area_map.width - ROOM_MAX_SIZE)
            w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            room = Rect(x, y, w, h)
            self._generate_monsters_in(room)
            self._generate_items_in(room)
            target -= 1

    def _find_empty_tile(self):
        while True:
            x = randint(0, self._area_map.width - 1)
            y = randint(0, self._area_map.height - 1)
            if self._area_map.tiles[x][y].is_walkable:
                break
        return x, y

    def _generate_monsters_in(self, room):
        # choose random number of monsters
        num_monsters = randint(0, MAX_ROOM_MONSTERS)

        for i in range(num_monsters):
            # choose random spot for this monster
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # only place it if the tile is not blocked
            if self._area_map.is_walkable(x, y):
                choice = randint(0, 100)
                if choice <= 55:  # 55%
                    name = 'bushslime'
                    data = config.data.enemies.bushslime
                    colour = colors.desaturated_green
                elif choice <= 85:  # 30%
                    name = 'steelhawk'
                    data = config.data.enemies.steelhawk
                    colour = colors.light_blue
                else:  # 15%
                    name = 'tigerslash'
                    data = config.data.enemies.tigerslash
                    colour = colors.orange

                monster = monster_factory.create_monster(data, x, y, colour, name)
                self._area_map.entities.append(monster)

    def _generate_items_in(self, room):
        # choose random number of items
        num_items = randint(0, MAX_ROOM_ITEMS)

        for i in range(num_items):
            # choose random spot for this item
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # only place it if the tile is not blocked
            if self._area_map.is_walkable(x, y):
                dice = randint(0, 100)
                if dice < 70:
                    # create a healing potion (70% chance)
                    char = '!'
                    name = 'healing potion'
                    color = colors.violet
                    use_func = cast_heal

                elif dice < 70 + 10:
                    # create a lightning bolt scroll (15% chance)
                    char = '#'
                    name = 'scroll of lightning bolt'
                    color = colors.light_yellow
                    use_func = cast_lightning

                elif dice < 70 + 10 + 10:
                    # create a fireball scroll (10% chance)
                    char = '#'
                    name = 'scroll of fireball'
                    color = colors.light_yellow
                    use_func = cast_fireball

                else:
                    # create a confuse scroll (15% chance)
                    char = '#'
                    name = 'scroll of confusion'
                    color = colors.light_yellow
                    use_func = cast_confuse

                item = item_factory.create_item(x, y, char, name, color, use_func)

                self._area_map.entities.append(item)
                item.send_to_back()  # items appear below other objects
