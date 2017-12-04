import unittest

from furusiya.ecs.entity import Entity
from furusiya.entities.player import Player
from furusiya.io.map_renderer import MapRenderer
from furusiya.maps.map import Map

class TestMapRenderer(unittest.TestCase):

    def test_fov_constants_are_reasonable(self):
        self.assertEqual(MapRenderer.FOV_ALGORITHM, 'BASIC')
        self.assertTrue(MapRenderer.SHOULD_LIGHT_WALLS)
        self.assertGreaterEqual(MapRenderer.VIEW_RADIUS, 5)

    def test_render_marks_current_fov_as_explored(self):
        map = Map(10, 10)
        # Sanity check: it's not explored yet
        self.assertFalse(map.tiles[0][0].is_explored)
        # Player is at (0, 0)
        renderer = MapRenderer(map, Player(), MockUiAdapter())
        renderer.render()
        # Just check straight horizontal/vertical, no need to check all tiles in FOV
        light_radius = MapRenderer.VIEW_RADIUS
        for i in range(light_radius):
            self.assertTrue(map.tiles[i][0].is_explored)
            self.assertTrue(map.tiles[0][i].is_explored)

    def test_render_recalculates_fov_when_asked(self):
        pass

    def test_render_draws_tiles_in_fov(self):
        pass

# Once finished, replace with: https://docs.python.org/3/library/unittest.mock.html
class MockUiAdapter:
    def render(self):
        pass

    def calculate_fov(self, *args):
        pass