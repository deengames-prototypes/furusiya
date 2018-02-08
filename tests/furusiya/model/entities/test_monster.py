from unittest.mock import Mock

import pytest

from model.components.ai.base import AI
from model.entities.monster import Monster


class AITest(AI):
    def __init__(self, owner=Mock()):
        super().__init__(owner)


class StunnedAI(AITest):
    pass


class WalkerAI(AITest):
    pass


@pytest.fixture
def monster():
    yield Monster(1, 1, 'n', 'test', (23, 54, 1))


@pytest.fixture
def stunned_ai():
    yield StunnedAI


@pytest.fixture
def walker_ai():
    yield WalkerAI


def test_replace_subcomponent(monster, stunned_ai, walker_ai):
    original = stunned_ai()
    monster.set_ai(original)
    assert monster.get_component(stunned_ai) == original

    replacer = walker_ai()
    monster.set_ai(replacer)

    assert monster.get_component(walker_ai) == replacer
    assert monster.get_component(stunned_ai) != original
    assert len(monster._components) == 1
