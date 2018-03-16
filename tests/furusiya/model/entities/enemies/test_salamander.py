from unittest.mock import Mock

import pytest

from game import Game
from model.entities.enemies.salamander import Salamander


class TestSalamander:
    @pytest.fixture
    def salamander(self):
        oldmap = Game.instance.area_map
        Game.instance.area_map = Mock()
        yield Salamander(2, 2, 's', 's', Mock())
        Game.instance.area_map = oldmap

    def test_spawn_fire_spawns_fire(self, salamander):
        Game.instance.area_map.get_walkable_tile_around.return_value = (2, 2)

        salamander.spawn_fire()

        assert Game.instance.area_map.entities.append.called
