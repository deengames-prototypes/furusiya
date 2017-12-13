import unittest

from furusiya.maps.area_map import AreaMap
from furusiya.ecs.entity import Entity
from furusiya.components.walkers.random_walker import RandomWalker

class TestRandomWalker(unittest.TestCase):

    def test_walk_walks_to_all_adjacencies(self):
        start_x, start_y = 3, 3
        area_map = AreaMap(start_x * 2, start_y * 2)
        entity = Entity((255, 255, 255), '@')
        entity.x, entity.y = (start_x, start_y)
        r = RandomWalker(area_map, entity)

        expected = [(start_x - 1, start_y), (start_x + 1, start_y), (start_x, start_y + 1), (start_x, start_y - 1)]
        iterations = 0

        while iterations < 1000 and expected:
            iterations += 1
            r.walk()
            actual = (entity.x, entity.y)
            if actual in expected:
                expected.remove(actual)

        self.assertGreater(iterations, 0, "1000 iterations and not all adjacencies were walked")
        self.assertEqual(len(expected), 0) # walked to all four adjacencies


    def test_walk_throws_if_all_adjacencies_are_unwalkable(self):
        area_map = AreaMap(5, 5)
        self.__make_unwalkable(area_map)

        entity = Entity((255, 255, 255), '@')
        entity.x, entity.y = (3, 2)
        area_map.tiles[entity.x][entity.y].is_walkable = True
        r = RandomWalker(area_map, entity)

        with self.assertRaises(ValueError):
            r.walk()


    def test_walk_doesnt_walk_off_the_map(self):
        area_map = AreaMap(5, 5)
        self.__make_unwalkable(area_map)

        entity = Entity((255, 255, 255), '@')
        r = RandomWalker(area_map, entity)

        # Set position to (0, 0) and everything to solid: should throw (shouldn't walk off the LHS/top)
        entity.x, entity.y = (0, 0)
        with self.assertRaises(ValueError):
            r.walk()

        # Set position to (width, height) and everything to solid, should throw (shouldn't walk off the RHS)
        entity.x, entity.y = (area_map.width - 1, area_map.height - 1)
        with self.assertRaises(ValueError):
            r.walk()

    
    def __make_unwalkable(self, area_map):
        for y in range(area_map.height):
            for x in range(area_map.width):
                area_map.tiles[x][y].is_walkable = False