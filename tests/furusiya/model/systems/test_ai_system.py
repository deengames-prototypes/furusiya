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
def owner1():
    yield Mock(id=1)


@pytest.fixture
def owner2():
    yield Mock(id=2)


@pytest.fixture
def owner3():
    yield Mock(id=3)


@pytest.fixture
def ai_sys(ai1, owner1, ai2, owner2, ai3, owner3):
    ai_sys = AISystem()

    ai_sys.set(owner1, ai1)
    ai_sys.set(owner2, ai2)
    ai_sys.set(owner3, ai3)

    yield ai_sys


def test_take_turn(ai_sys, ai1, owner1, ai2, owner2, ai3, owner3):
    for owner, ai in {owner1: ai1, owner2: ai2, owner3: ai3}.items():
        ai_sys.take_turn(owner)
        assert ai.take_turn.called
