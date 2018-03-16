from unittest.mock import Mock

import pytest

from game import Game
from model.entities.game_object import GameObject


class TestGameObject:
    @pytest.fixture
    def obj(self):
        yield GameObject(2, 2, 't', 'testObject', Mock())

    def test_die_unbinds_events_and_removes_self_from_entity_list(self, obj):
        Game.instance.area_map = Mock()
        Game.instance.event_bus = Mock()

        obj.die()

        assert Game.instance.area_map.entities.remove.called
        assert Game.instance.event_bus.unregister.called
