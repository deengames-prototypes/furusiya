import math
import random
import unittest

from game import Game
from model.maps.generators.forest_generator import ForestGenerator
from model.maps.area_map import AreaMap


class TestForestGenerator(unittest.TestCase):
    def test_generate_generates_trees(self):
        width, height = (10, 10)
        Game.area_map = AreaMap(width, height)
        fg = ForestGenerator(Game.area_map)
        expected_num_trees = math.floor(ForestGenerator.TREE_PERCENTAGE * width * height)

        actual_num_trees = 0

        for y in range(height):
            for x in range(width):
                if not Game.area_map.tiles[x][y].is_walkable:
                    actual_num_trees += 1

        # might be more trees because of filled gaps between trees
        self.assertGreaterEqual(actual_num_trees, expected_num_trees)

    def test_generate_fills_holes(self):
        
        # Generate a bunch of trees with a known seed that generates holes.
        # This is fragile, but there's no other way to test this.
        # This is valuable, because there's a ton of code/complexity behind
        # this (breadth-first search, etc.).
        width, height = (60, 40)
        Game.area_map = AreaMap(width, height)
        fg = ForestGenerator(Game.area_map)
        pre_fill_num_trees = math.floor(ForestGenerator.TREE_PERCENTAGE * width * height)

        random.seed(1)

        actual_num_trees = 0

        for y in range(height):
            for x in range(width):
                if not Game.area_map.tiles[x][y].is_walkable:
                    actual_num_trees += 1

        # Strictly more trees because of filled holes
        # With 60x40 and seed=1, fills 6 gaps with trees
        self.assertGreater(actual_num_trees, pre_fill_num_trees)

    def test_generate_generates_monsters(self):
        width, height = 10, 10
        Game.area_map = AreaMap(width, height)
        fg = ForestGenerator(Game.area_map)

        self.assertTrue(fg._area_map is Game.area_map)
        self.assertGreaterEqual(len(Game.area_map.entities), 1)
