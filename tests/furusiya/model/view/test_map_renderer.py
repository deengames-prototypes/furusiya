import unittest
from unittest.mock import MagicMock

from constants import FOV_ALGO, FOV_LIGHT_WALLS
from main_interface import Game
from model.entities.party.player import Player
from model.config import config
from model.maps.area_map import AreaMap
from view.map_renderer import MapRenderer
from view.adapter.tdl_adapter import TdlAdapter


screen_width = 50
screen_height = 50
map_width = 10
map_height = 10
panel_height = 5


class TestMapRenderer(unittest.TestCase):
    def test_render_marks_current_fov_as_explored(self):
        map = AreaMap(map_width, map_height)

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

        tdl_adapter = TdlAdapter(
            "Test Window",
            map=(map_width, map_height),
            screen=(screen_width, screen_height),
            panel=(screen_width, panel_height)
        )
        tdl_adapter.calculate_fov = MagicMock(return_value=fov_tiles)

        renderer = MapRenderer(map, player, tdl_adapter)
        Game.renderer = renderer
        Game.ui = tdl_adapter
        renderer.render()

        # Just check straight horizontal/vertical, as per our expectation
        for (x, y) in fov_tiles:
            self.assertTrue(map.tiles[x][y].is_explored)

    def test_render_recalculates_fov_when_asked(self):
        map = AreaMap(map_width, map_height)

        # Player is at (0, 0)
        player = Player()

        # Mock the FOV tiles.
        light_radius = config.data.player.lightRadius
        fov_tiles = []        

        for i in range(light_radius):
            fov_tiles.append((i, 0))  # horizontal ray
            fov_tiles.append((0, i))  # vertical ray

        tdl_adapter = TdlAdapter(
            "Test Window",
            map=(map_width, map_height),
            screen=(screen_width, screen_height),
            panel=(screen_width, panel_height)
        )
        tdl_adapter.calculate_fov = MagicMock(return_value=fov_tiles)

        renderer = MapRenderer(map, player, tdl_adapter)
        self.assertTrue(renderer.recompute_fov)
        Game.renderer = renderer
        Game.ui = tdl_adapter
        renderer.render()  # calls calculate_fov
        
        self.assertFalse(renderer.recompute_fov)        
        tdl_adapter.calculate_fov.reset_mock()  # reset call count to 0
        renderer.render()  # doesn't call calculate_fov
        tdl_adapter.calculate_fov.assert_not_called()

        renderer.recompute_fov = True
        renderer.render()

        tdl_adapter.calculate_fov.assert_called_with(
            player.x, player.y, map.is_visible_tile, FOV_ALGO, light_radius, FOV_LIGHT_WALLS
        )
