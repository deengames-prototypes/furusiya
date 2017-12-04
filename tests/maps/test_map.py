import math
import random
import unittest

from furusiya.ecs.entity import Entity
from furusiya.maps.generators.forest_generator import ForestGenerator
from furusiya.maps.map import Map

class TestMap(unittest.TestCase):
    def test_place_on_random_ground_places_entity_on_random_ground(self):
        width, height = (10, 10)
        map = Map(width, height)        
        fg = ForestGenerator(width, height)
        fg.generate_trees(map)

        e = Entity('a', (255, 0, 0))
        map.place_on_random_ground(e)
        
        self.assertEqual(map.tiles[e.x][e.y].is_walkable, True)

    def test_is_walkable_returns_true_for_empty_ground_within_bounds(self):
        map = Map(10, 10)
        map.tiles[0][0].is_walkable = False

        self.assertFalse(map.is_walkable(0, 0))
        self.assertTrue(map.is_walkable(5, 5))
        # off-map? not walkable.
        self.assertFalse(map.is_walkable(-1, 6))
        self.assertFalse(map.is_walkable(150, 5))
        self.assertFalse(map.is_walkable(2, -17))
        self.assertFalse(map.is_walkable(3, 77))

    def test_is_walkable_returns_false_if_entity_is_there(self):
        map = Map(10, 10)
        e = Entity('@', (0, 0, 0))
        map.place_on_random_ground(e)
        self.assertFalse(map.is_walkable(e.x, e.y))
        