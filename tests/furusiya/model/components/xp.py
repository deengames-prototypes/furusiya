from unittest.mock import Mock

import pytest

import game
from model.components.xp import XPComponent
from model.systems.fighter_system import FighterSystem


@pytest.fixture
def player():
    yield Mock()


@pytest.fixture
def player_fighter():
    yield Mock(max_hp=30)


@pytest.fixture
def xp(monkeypatch, player, player_fighter):
    FighterSystem.set_fighter(player, player_fighter)
    monkeypatch.setattr(game, 'message', lambda *args, **kwargs: None)
    yield XPComponent(player)


def test_gain_xp(xp, player_fighter):
    old_level = xp.level
    xp.gain_xp(xp._xp_next_level())

    assert xp.level == old_level + 1
    player_fighter.assert_called_with(player_fighter.max_hp)


def test_level_up_multiple_times(xp):
    old_level = xp.level
    xp.gain_xp(1000)

    assert xp.level > old_level + 2
