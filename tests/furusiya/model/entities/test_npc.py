from unittest.mock import Mock

import pytest

from model.components.ai.base import AI
from model.entities.npc import NPC


class AITest(AI):
    def __init__(self, owner=Mock()):
        super().__init__(owner)


class StunnedAI(AITest):
    pass


class WalkerAI(AITest):
    pass


@pytest.fixture
def npc():
    yield NPC(1, 1, 'n', 'test', (23, 54, 1))


@pytest.fixture
def stunned_ai():
    yield StunnedAI


@pytest.fixture
def walker_ai():
    yield WalkerAI


def test_replace_subcomponent(npc, stunned_ai, walker_ai):
    original = stunned_ai()
    npc.set_ai(original)
    assert npc.get_component(stunned_ai) == original

    replacer = walker_ai()
    npc.set_ai(replacer)

    assert npc.get_component(walker_ai) == replacer
    assert npc.get_component(stunned_ai) != original
    assert len(npc._components) == 1
