from unittest.mock import Mock

import pytest

from game import Game
from model.components.xp import XPComponent
from model.entities.game_object import GameObject
from model.helper_functions.death_functions import monster_death
from model.systems.ai_system import AISystem
from model.systems.fighter_system import FighterSystem
from model.systems.xp_system import XPSystem


MONSTER_XP = 50


@pytest.fixture
def monster():
    obj = GameObject(2, 2, 's', 'scary monster', (0, 0, 0), blocks=True, hostile=True)

    XPSystem.set_experience(obj, Mock(xp=MONSTER_XP))
    FighterSystem.set_fighter(obj, Mock())
    AISystem.set_ai(obj, Mock())

    yield obj


@pytest.fixture
def player():
    XPSystem.set_experience(Game.player, XPComponent(Game.player))

    yield Game.player


def test_monster_death_marks_monster_as_dead(monster, player):
    playerxp = XPSystem.get_experience(player)
    old_xp = playerxp.xp

    monster_death(monster)
    new_xp = playerxp.xp

    assert monster.char == '%'
    assert monster.blocks is False
    assert monster.hostile is False

    assert new_xp > old_xp

    assert not FighterSystem.has_fighter(monster)
    assert not AISystem.has_ai(monster)
