from unittest.mock import Mock

import pytest

from model.components.ai.base import AI
from model.entities.npc import NPC


class AITest(AI):
    def __init__(self, owner=Mock()):
        super().__init__(owner)


class AITest1(AITest):
    pass


class AITest2(AITest):
    pass


@pytest.fixture
def npc():
    yield NPC(1, 1, 'n', 'test', (23, 54, 1))


@pytest.fixture
def ai1():
    yield AITest1


@pytest.fixture
def ai2():
    yield AITest2


def test_replace_subcomponent(npc, ai1, ai2):
    original = ai1()
    npc.set_ai(original)
    assert npc.get_component(AI) == original

    replacer = ai2()
    npc.set_ai(replacer)

    assert npc.get_component(AI) == replacer
    assert npc.get_component(AI) != original
    assert len(npc._components) == 1
