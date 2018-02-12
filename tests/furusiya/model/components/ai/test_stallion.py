from unittest.mock import MagicMock

import math
import pytest

from model.components.ai.stallion import StallionAi


@pytest.fixture
def stallion():
    stallion_mock = MagicMock(x=2, y=0)
    stallion_mock.is_mounted = False

    def move_towards(x, y):  # copypaste from game_object.py
        dx = x - stallion_mock.x
        dy = y - stallion_mock.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        stallion_mock.x, stallion_mock.y = dx, dy

    stallion_mock.move_towards.side_effect = move_towards
    stallion_mock.player = MagicMock(x=4, y=1)
    stallion_mock.ai = StallionAi(stallion_mock)
    yield stallion_mock


def test_take_turn_far(stallion):
    stallion.distance_to.return_value = 5

    original = (stallion.x, stallion.y)

    stallion.ai.take_turn()
    stallion.move_towards.assert_called_with(stallion.player.x, stallion.player.y)
    assert (stallion.x, stallion.y) != original


def test_take_turn_close(stallion):
    stallion.distance_to.return_value = 1

    original = (stallion.x, stallion.y)

    stallion.ai.take_turn()
    assert stallion.move_towards.call_count == 0
    assert (stallion.x, stallion.y) == original


def test_take_turn_mounted(stallion):
    stallion.is_mounted = True
    stallion.ai.take_turn()

    assert (stallion.x, stallion.y) == (stallion.player.x, stallion.player.y)
