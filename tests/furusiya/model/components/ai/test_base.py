from unittest.mock import Mock

import pytest

from game import Game
from model.components.ai.base import AbstractAI
from model.systems.system import ComponentSystem


class TestAbstractAI:
    @pytest.fixture
    def ai(self):
        Game.ai_system = ComponentSystem()
        test_ai = AbstractAI(Mock())
        Game.ai_system.set(test_ai.owner, test_ai)
        yield test_ai

    def test_temporarily_switch_to_switches_to_another_ai(self, ai):
        num_turns = 5
        other = AbstractAI(Mock(), num_turns)

        def _take_turn(): other.num_turns -= 1
        other._take_turn = _take_turn

        ai.temporarily_switch_to(other)

        for _ in range(num_turns):
            assert Game.ai_system.get(ai.owner) is other
            other.take_turn()

        other.take_turn()  # one more time to remove old AI
        assert Game.ai_system.get(ai.owner) is ai

    def test_temporarily_switch_to_extends_current_ai(self, ai):
        num_turns = 5
        other = AbstractAI(Mock(), num_turns)
        ai.num_turns = old_num_turns = num_turns

        ai.temporarily_switch_to(other)

        assert Game.ai_system.get(ai.owner) is ai
        assert ai.num_turns == old_num_turns + num_turns

    def test_temporary_take_turn_takes_turn_if_turns_left(self, ai):
        num_turns = 5
        ai.take_turn = Mock()
        ai.other = Mock()
        ai.other.num_turns = num_turns
        Game.ai_system.set(ai.owner, Mock())

        def other_take_turn(): ai.other.num_turns -= 1
        ai.other._take_turn.side_effect = other_take_turn

        for _ in range(num_turns):
            ai.temporary_take_turn()
            assert ai.other._take_turn.called
            ai.other._take_turn.reset_mock()

        ai.temporary_take_turn()
        assert ai.other.cleanup.called
        assert ai.take_turn.called
        assert Game.ai_system.get(ai.owner) is ai
