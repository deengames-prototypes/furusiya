import unittest

from model.game_object import GameObject
from model.maps.area_map import AreaMap
from model.maps.generators.forest_generator import ForestGenerator


class TestMap(unittest.TestCase):
    def test_place_on_random_ground_places_entity_on_random_ground(self):
        width, height = (10, 10)
        basic_map = AreaMap(width, height)        
        fg = ForestGenerator(width, height, basic_map)

        e = GameObject(0, 0, 'a', 'test', (255, 0, 0))
        basic_map.place_on_random_ground(e)
        
        self.assertEqual(basic_map.tiles[e.x][e.y].is_walkable, True)

    def test_is_walkable_returns_true_for_empty_ground_within_bounds(self):
        basic_map = AreaMap(10, 10)
        basic_map.tiles[0][0].is_walkable = False

        self.assertFalse(basic_map.is_walkable(0, 0))
        self.assertTrue(basic_map.is_walkable(5, 5))
        # off-basic_map? not walkable.
        self.assertFalse(basic_map.is_walkable(-1, 6))
        self.assertFalse(basic_map.is_walkable(150, 5))
        self.assertFalse(basic_map.is_walkable(2, -17))
        self.assertFalse(basic_map.is_walkable(3, 77))

    def test_is_walkable_returns_false_if_entity_is_there(self):
        basic_map = AreaMap(10, 10)
        e = GameObject(0, 0, '@', 'player', (0, 0, 0))
        basic_map.place_on_random_ground(e)
        self.assertFalse(basic_map.is_walkable(e.x, e.y))
