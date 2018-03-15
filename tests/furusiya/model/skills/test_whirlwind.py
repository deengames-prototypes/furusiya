from unittest.mock import Mock

import math
import pytest

from game import Game
from model.skills.whirlwind import Whirlwind


def _mock_factory(*args, fighter=None, **kwargs):
    fighter = fighter or Mock()
    m = Mock(*args, **kwargs)
    Game.instance.fighter_system.set(m, fighter)
    m.distance.side_effect = lambda x, y: math.sqrt((x - m.x) ** 2 + (y - m.y) ** 2)
    return m


@pytest.fixture
def whirlwind():
    yield Whirlwind


def test_process(whirlwind):
    player_fighter = Mock()
    player = _mock_factory(x=1, y=2, fighter=player_fighter)

    bushslime = _mock_factory(x=7, y=8)
    tigerslash = _mock_factory(x=2, y=2)
    steelhawk = _mock_factory(x=2, y=1)

    whirlwind.process(player, 2, Mock(entities=[player, bushslime, tigerslash, steelhawk]))

    player_fighter.attack.assert_any_call(tigerslash)
    player_fighter.attack.assert_any_call(steelhawk)

    with pytest.raises(AssertionError):
        player_fighter.attack.assert_called_with(player)

    with pytest.raises(AssertionError):
        player_fighter.attack.assert_called_with(bushslime)
