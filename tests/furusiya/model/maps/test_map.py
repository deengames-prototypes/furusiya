import pytest

from game import Game
from model.entities.game_object import GameObject
from model.maps.area_map import AreaMap
from model.maps.generators.forest_generator import ForestGenerator
from model.rect import Rect


class TestMap:
    @pytest.fixture
    def basic_map(self):
        yield AreaMap(10, 10)

    @pytest.fixture
    def blocked_map(self, basic_map):
        for tile_row in basic_map.tiles:
            for tile in tile_row:
                tile.is_walkable = False

        yield basic_map

    def test_place_on_random_ground_places_entity_on_random_ground(self):
        width, height = (10, 10)
        Game.area_map = AreaMap(width, height)
        fg = ForestGenerator(Game.area_map)

        e = GameObject(0, 0, 'a', 'test', (255, 0, 0))
        Game.area_map.place_on_random_ground(e)
        
        assert Game.area_map.tiles[e.x][e.y].is_walkable is True

    def test_is_walkable_returns_true_for_empty_ground_within_bounds(self, basic_map):
        basic_map.tiles[0][0].is_walkable = False

        assert not basic_map.is_walkable(0, 0)
        assert basic_map.is_walkable(5, 5)
        # off-basic_map? not walkable.
        assert not basic_map.is_walkable(-1, 6)
        assert not basic_map.is_walkable(150, 5)
        assert not basic_map.is_walkable(2, -17)
        assert not basic_map.is_walkable(3, 77)

    def test_is_walkable_returns_false_if_entity_is_there(self, basic_map):
        e = GameObject(0, 0, '@', 'player', (0, 0, 0), blocks=True)
        basic_map.place_on_random_ground(e)
        assert not basic_map.is_walkable(e.x, e.y)

    def test_get_blocking_object_at_returns_object_if_object_is_there(self, basic_map):
        e = GameObject(0, 0, '@', 'player', (0, 0, 0), blocks=True)
        basic_map.place_on_random_ground(e)

        # Act
        blocking_object = basic_map.get_blocking_object_at(e.x, e.y)

        # Assert
        assert e is blocking_object

    def test_get_blocking_object_at_returns_none_if_nothing_is_there(self, basic_map):
        # Act
        blocking_object = basic_map.get_blocking_object_at(0, 0)

        # Assert
        assert blocking_object is None

    def test_get_walkable_tile_within_gets_tile_if_available(self, basic_map):
        # block top-left corner
        basic_map.tiles[2][2].is_walkable = False
        basic_map.tiles[3][2].is_walkable = False
        basic_map.tiles[2][3].is_walkable = False

        rect = Rect(2, 2, 4, 4)

        # Act
        tile = basic_map.get_walkable_tile_within(rect)

        # Assert
        assert tile is not None
        assert tile in ((x, y) for x in range(rect.x1, rect.x2) for y in range(rect.y1, rect.y2))
        assert basic_map.tiles[tile[0]][tile[1]].is_walkable

    def test_get_walkable_tile_within_returns_none_if_not_available(self, blocked_map):
        rect = Rect(2, 2, 4, 4)

        # Act
        tile = blocked_map.get_walkable_tile_within(rect)

        # Assert
        assert tile is None

    def test_get_walkable_tile_around_gets_tile_if_available(self, basic_map):
        x, y, range_num = 2, 2, 4
        basic_map.tiles[x][y].is_walkable = False

        # Act
        tile = basic_map.get_walkable_tile_around(x, y, range_num)

        # Assert
        assert tile is not None
        assert tile in (
            (tile[0] + dx, tile[1] + dy)
            for dx in range(-range_num, range_num + 1)
            for dy in range(-range_num, range_num + 1)
        )  # is in range
        assert basic_map.tiles[tile[0]][tile[1]].is_walkable

    def test_get_walkable_tile_around_returns_none_if_not_available(self, blocked_map):
        x, y, range_num = 2, 2, 4

        # Act
        tile = blocked_map.get_walkable_tile_around(x, y, range_num)

        # Assert
        assert tile is None
