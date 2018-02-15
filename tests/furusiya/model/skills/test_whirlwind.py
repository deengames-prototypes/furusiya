from unittest.mock import Mock

import math
import pytest

from model.skills.whirlwind import Whirlwind
from model.systems.fighter_system import FighterSystem


def _mock_factory(*args, **kwargs):
    m = Mock(*args, **kwargs)
    m.distance.side_effect = lambda x, y: math.sqrt((x - m.x) ** 2 + (y - m.y) ** 2)
    return m


@pytest.fixture
def player():
    yield _mock_factory(x=1, y=2)


@pytest.fixture
def player_fighter():
    yield Mock()


@pytest.fixture
def bushslime():
    yield _mock_factory(x=7, y=8)


@pytest.fixture
def _fighter():
    yield Mock()


@pytest.fixture
def tigerslash():
    yield _mock_factory(x=2, y=2)


@pytest.fixture
def whirlwind(player, player_fighter, bushslime, tigerslash, _fighter):
    FighterSystem.set_fighter(player, player_fighter)
    FighterSystem.set_fighter(bushslime, _fighter)
    FighterSystem.set_fighter(tigerslash, _fighter)
    yield Whirlwind


def test_process(whirlwind, player, player_fighter, tigerslash, bushslime):
    whirlwind.process(player, 2, Mock(entities=[player, bushslime, tigerslash]))

    player_fighter.attack.assert_called_with(tigerslash)

    with pytest.raises(AssertionError):
        player_fighter.attack.assert_called_with(player)

    with pytest.raises(AssertionError):
        player_fighter.attack.assert_called_with(bushslime)
