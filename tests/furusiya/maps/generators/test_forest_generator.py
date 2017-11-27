import math
import unittest

from src.furusiya.maps.generators.forest_generator import ForestGenerator
from src.furusiya.maps.map import Map

class TestForestGenerator(unittest.TestCase):
    def test_generate_trees_generates_trees(self):
        width, height = (10, 10)
        map = Map(width, height)        
        fg = ForestGenerator(width, height)
        expected_num_trees = math.floor(ForestGenerator.TREE_PERCENTAGE * width * height)

        fg.generate_trees(map)

        actual_num_trees = 0

        for y in range(height):
            for x in range(width):
                if map.tiles[x][y].is_walkable == False:
                    actual_num_trees += 1

        # might be more trees because of filled gaps between trees
        self.assertGreaterEqual(actual_num_trees, expected_num_trees)
