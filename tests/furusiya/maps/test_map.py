import math
import random
import unittest

from src.ecs.entity import Entity
from src.furusiya.maps.generators.forest_generator import ForestGenerator
from src.furusiya.maps.map import Map

class TestMap(unittest.TestCase):
    def test_place_on_random_ground_places_entity_on_random_ground(self):
        width, height = (10, 10)
        map = Map(width, height)        
        fg = ForestGenerator(width, height)
        fg.generate_trees(map)

        e = Entity('a', (255, 0, 0))
        map.place_on_random_ground(e)
        
        self.assertEqual(map.tiles[e.x][e.y].is_walkable, True)