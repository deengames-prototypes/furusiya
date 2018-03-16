import pytest

from game import Game
from model.maps.generators.dungeon_generator import DungeonGenerator
from model.maps.area_map import AreaMap
from model.entities.party.player import Player


class TestDungeonGenerator:
    @pytest.fixture
    def dg(self):
        Game()
        Game.instance.area_map = AreaMap(80, 43)
        Game.instance.player = Player()
        Game.instance.area_map.place_on_random_ground(Game.instance.player)
        dungeongen = DungeonGenerator(Game.instance.area_map)
        dungeongen.generate()
        yield dungeongen

    def test_generate_generates_rooms(self, dg):
        assert len(dg._rooms) > 0
        # Basic sanity
        for room in dg._rooms:
            assert room.x1 >= 0
            assert room.y1 >= 0
            assert room.x2 > room.x1
            assert room.y2 > room.y1
            assert room.x2 - room.x1 >= 3  # two walls and a space in between
            assert room.y2 - room.y1 >= 3  # two walls and a space in between

    def test_generate_generates_monsters(self, dg):
        assert dg._area_map is Game.instance.area_map
        assert len(Game.instance.area_map.entities) >= 1
