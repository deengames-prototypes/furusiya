from unittest.mock import Mock

import pytest

from game import Game
from model.components.xp import XPComponent
from model.entities.game_object import GameObject
from model.helper_functions.death_functions import monster_death, player_death


MONSTER_XP = 50


@pytest.fixture
def monster():
    obj = GameObject(2, 2, 's', 'scary monster', (0, 0, 0), blocks=True, hostile=True)

    Game.xp_sys.set(obj, Mock(xp=MONSTER_XP))
    Game.fighter_system.set(obj, Mock())
    Game.ai_system.set(obj, Mock())

    yield obj


@pytest.fixture
def player():
    Game.xp_sys.set(Game.player, XPComponent(Game.player))
    Game.keybinder = Mock()

    yield Game.player


def test_monster_death_marks_monster_as_dead(monster, player):
    playerxp = Game.xp_sys.get(player)
    old_xp = playerxp.xp

    monster_death(monster)
    new_xp = playerxp.xp

    assert monster.char == '%'
    assert monster.blocks is False
    assert monster.hostile is False

    assert new_xp > old_xp

    assert not Game.fighter_system.has(monster)
    assert not Game.ai_system.has(monster)


def test_player_death_affects_game_state(player):
    Game.game_state = 'playing'

    player_death(player)

    assert Game.game_state == 'dead'
    assert player.char == '%'
