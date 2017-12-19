from furusiya.maps.area_map import AreaMap
from furusiya.entities.monster import Monster
from furusiya.entities.player import Player
import unittest

class TestMonster(unittest.TestCase):
    def setUp(self):
        p = Player() # sets up Player.INSTANCE
        # Player should be far away so that monsters move
        p.x = 999
        p.y = 999

    def test_walk_moves_the_monster(self):
        area_map = AreaMap(6, 6)
        m = Monster('a', (255, 0, 0), area_map)
        m.x, m.y = 3, 3

        m.walk()
        self.assertTrue(
            (m.x == 3 and m.y in [2, 4]) or
            (m.x in [2, 4] and m.y == 3)
        )

    def test_walk_throws_if_all_adjacencies_are_unwalkable(self):
        area_map = AreaMap(6, 6)
        for y in range(area_map.height):
            for x in range(area_map.width):
                area_map.tiles[x][y].is_walkable = False

        # Don't need the current position to be walkable
        m = Monster('b', (0, 0, 255), area_map)
        m.x, m.y = 2, 2

        with self.assertRaises(ValueError):
            m.walk()

