import unittest

from game import Game
from model.entities.game_object import GameObject
from model.maps.area_map import AreaMap
from model.maps.generators.forest_generator import ForestGenerator


class TestMap(unittest.TestCase):
    def test_place_on_random_ground_places_entity_on_random_ground(self):
        width, height = (10, 10)
        Game.area_map = AreaMap(width, height)
        fg = ForestGenerator(Game.area_map)

        e = GameObject(0, 0, 'a', 'test', (255, 0, 0))
        Game.area_map.place_on_random_ground(e)
        
        self.assertEqual(Game.area_map.tiles[e.x][e.y].is_walkable, True)

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
        e = GameObject(0, 0, '@', 'player', (0, 0, 0), blocks=True)
        basic_map.place_on_random_ground(e)
        self.assertFalse(basic_map.is_walkable(e.x, e.y))

    def test_get_blocking_object_at_returns_object_if_object_is_there(self):
        basic_map = AreaMap(10, 10)
        e = GameObject(0, 0, '@', 'player', (0, 0, 0), blocks=True)
        basic_map.place_on_random_ground(e)

        # Act
        blocking_object = basic_map.get_blocking_object_at(e.x, e.y)

        # Assert
        self.assertIs(e, blocking_object)

    def test_get_blocking_object_at_returns_none_if_nothing_is_there(self):
        basic_map = AreaMap(10, 10)

        # Act
        blocking_object = basic_map.get_blocking_object_at(0, 0)

        # Assert
        self.assertIsNone(blocking_object)
