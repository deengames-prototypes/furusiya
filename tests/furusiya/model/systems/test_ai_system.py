from unittest.mock import Mock

import pytest

from model.systems.ai_system import AISystem


@pytest.fixture
def ai_sys():
    AISystem.ais = {}
    yield AISystem


def test_basic(ai_sys):
    owner1, ai1 = 'owner1', Mock()
    ai_sys.set_ai(owner1, ai1)

    assert ai_sys.has_ai(owner1)
    assert ai_sys.get_ai(owner1) == ai1

    owner2, ai2 = 'owner2', Mock()
    ai_sys.set_ai(owner2, ai2)
    owner3, ai3 = 'owner3', Mock()
    ai_sys.set_ai(owner3, ai3)

    ai_sys.take_monster_turns()

    for ai in (ai1, ai2, ai3):
        assert ai.take_turn.called

    ai_sys.remove_ai(owner1)
    assert not ai_sys.has_ai(owner1)
    assert ai_sys.get_ai(owner1) is None
