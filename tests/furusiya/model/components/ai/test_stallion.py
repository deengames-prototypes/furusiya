from unittest.mock import MagicMock

import pytest

from model.components.ai.stallion import StallionAi


@pytest.fixture
def stallion():
    stallion_mock = MagicMock(x=2, y=0)
    stallion_mock.is_mounted = False
    stallion_mock.player = MagicMock(x=4, y=1)
    stallion_mock.ai = StallionAi(stallion_mock)
    yield stallion_mock


def test_take_turn_far(stallion):
    stallion.distance_to.return_value = 5
    stallion.ai.take_turn()

    stallion.move_towards.assert_called_with(stallion.player.x, stallion.player.y)


def test_take_turn_close(stallion):
    stallion.distance_to.return_value = 1
    stallion.ai.take_turn()

    assert stallion.move_towards.call_count == 0


def test_take_turn_mounted(stallion):
    stallion.is_mounted = True
    stallion.ai.take_turn()

    assert (stallion.x, stallion.y) == (stallion.player.x, stallion.player.y)
