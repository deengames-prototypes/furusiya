from unittest.mock import Mock

import pytest

from model.systems.ai_system import AISystem


@pytest.fixture
def ai1():
    yield Mock()


@pytest.fixture
def ai2():
    yield Mock()


@pytest.fixture
def ai3():
    yield Mock()


@pytest.fixture
def ai_sys(ai1, ai2, ai3):
    AISystem.ais = {}

    AISystem.set_ai('owner1', ai1)
    AISystem.set_ai('owner2', ai2)
    AISystem.set_ai('owner3', ai3)

    yield AISystem


def test_take_turn(ai_sys, ai1, ai2, ai3):
    for owner, ai in {'owner1': ai1, 'owner2': ai2, 'owner3': ai3}.items():
        ai_sys.take_turn(owner)
        assert ai.take_turn.called
