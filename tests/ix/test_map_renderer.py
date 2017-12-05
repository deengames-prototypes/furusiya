import unittest

from furusiya.ecs.entity import Entity
from furusiya.entities.player import Player
from furusiya.io.map_renderer import MapRenderer
from furusiya.io.adapters.tdl_adapter import TdlAdapter
from furusiya.maps.map import Map
from unittest.mock import MagicMock
from unittest.mock import patch

class TestMapRenderer(unittest.TestCase):

    def test_fov_constants_are_reasonable(self):
        self.assertEqual(MapRenderer.FOV_ALGORITHM, 'BASIC')
        self.assertTrue(MapRenderer.SHOULD_LIGHT_WALLS)
        self.assertGreaterEqual(MapRenderer.VIEW_RADIUS, 5)

    def test_render_marks_current_fov_as_explored(self):
        map_width = 10
        map_height = 10
        map = Map(map_width, map_height)

        # Player is at (0, 0)
        player = Player()

        # Mock the FOV tiles.
        light_radius = 5
        fov_tiles = []        

        for i in range(light_radius):
            fov_tiles.append((i, 0)) # horizontal ray
            fov_tiles.append((0, i)) # vertical ray

        # Sanity check: it's not explored yet
        for (x, y) in fov_tiles:
            self.assertFalse(map.tiles[x][y].is_explored)

        tdl_adapter = TdlAdapter("Test Window", map_width, map_height)
        tdl_adapter.calculate_fov = MagicMock(return_value = fov_tiles)

        renderer = MapRenderer(map, player, tdl_adapter)
        renderer.render()

        # Just check straight horizontal/vertical, as per our expectation
        for (x, y) in fov_tiles:
            self.assertTrue(map.tiles[x][y].is_explored)

    def test_render_recalculates_fov_when_asked(self):
        map_width = 10
        map_height = 10
        map = Map(map_width, map_height)

        # Player is at (0, 0)
        player = Player()

        # Mock the FOV tiles.
        light_radius = 5
        fov_tiles = []        

        for i in range(light_radius):
            fov_tiles.append((i, 0)) # horizontal ray
            fov_tiles.append((0, i)) # vertical ray

        tdl_adapter = TdlAdapter("Test Window", map_width, map_height)
        tdl_adapter.calculate_fov = MagicMock(return_value = fov_tiles)

        renderer = MapRenderer(map, player, tdl_adapter)
        self.assertTrue(renderer.recompute_fov)
        renderer.render() # calls calculate_fov
        
        self.assertFalse(renderer.recompute_fov)        
        tdl_adapter.calculate_fov.reset_mock() # reset call count to 0
        renderer.render() # doesn't call calculate_fov
        tdl_adapter.calculate_fov.assert_not_called()

        renderer.recompute_fov = True
        renderer.render()

        tdl_adapter.calculate_fov.assert_called_with(player.x, player.y, map.is_walkable,
            MapRenderer.FOV_ALGORITHM, light_radius, MapRenderer.SHOULD_LIGHT_WALLS)