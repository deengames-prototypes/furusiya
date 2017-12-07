import math
import random
import unittest

from furusiya.maps.generators.forest_generator import ForestGenerator
from furusiya.maps.map import Map

class TestForestGenerator(unittest.TestCase):
    def test_generate_generates_trees(self):
        width, height = (10, 10)
        map = Map(width, height)        
        fg = ForestGenerator(width, height)
        expected_num_trees = math.floor(ForestGenerator.TREE_PERCENTAGE * width * height)

        fg.generate(map)

        actual_num_trees = 0

        for y in range(height):
            for x in range(width):
                if map.tiles[x][y].is_walkable == False:
                    actual_num_trees += 1

        # might be more trees because of filled gaps between trees
        self.assertGreaterEqual(actual_num_trees, expected_num_trees)

    def test_generate_fills_holes(self):
        
        # Generate a bunch of trees with a known seed that generates holes.
        # This is fragile, but there's no other way to test this.
        # This is valuable, because there's a ton of code/complexity behind
        # this (breadth-first search, etc.).
        width, height = (60, 40)
        map = Map(width, height)        
        fg = ForestGenerator(width, height)
        pre_fill_num_trees = math.floor(ForestGenerator.TREE_PERCENTAGE * width * height)

        random.seed(1)
        fg.generate(map)

        actual_num_trees = 0

        for y in range(height):
            for x in range(width):
                if map.tiles[x][y].is_walkable == False:
                    actual_num_trees += 1

        # Strictly more trees because of filled holes
        # With 60x40 and seed=1, fills 6 gaps with trees
        self.assertGreater(actual_num_trees, pre_fill_num_trees)
