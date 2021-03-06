from game import Game
from model.keys.decorators import in_game, skill
from model.components.skill import SkillComponent
import pytest
from unittest.mock import Mock

class TestInGameDecorator:
    @pytest.fixture(autouse=True, scope='class')
    def setup_state(self):
        Game.instance.game_state = 'playing'
        Game.instance.current_turn = Game.instance.player

    def test_in_game_callback_only_calls_in_game(self):
        actual_function = Mock()
        mock_event = Mock()

        doesnt_pass_turn = in_game(actual_function, pass_turn=False)
        doesnt_pass_turn(mock_event)
        assert Game.instance.current_turn is Game.instance.player
        actual_function.assert_called_with(mock_event)

        actual_function.reset_mock()

        passes_turn = in_game(actual_function, pass_turn=True)
        passes_turn(mock_event)
        assert Game.instance.current_turn is None
        actual_function.assert_called_with(mock_event)

    def test_in_game_callback_doesnt_call_when_not_in_game(self):
        Game.instance.game_state = 'dead'

        actual_function = Mock()
        mock_event = Mock()

        doesnt_pass_turn = in_game(actual_function, pass_turn=False)
        doesnt_pass_turn(mock_event)
        actual_function.assert_not_called()

        actual_function.reset_mock()

        passes_turn = in_game(actual_function, pass_turn=True)
        passes_turn(mock_event)
        actual_function.assert_not_called()

    def test_in_game_callback_doesnt_call_when_not_player_turn(self):
        Game.instance.current_turn = None

        actual_function = Mock()
        mock_event = Mock()

        doesnt_pass_turn = in_game(actual_function, pass_turn=False)
        doesnt_pass_turn(mock_event)
        actual_function.assert_not_called()

        actual_function.reset_mock()

        passes_turn = in_game(actual_function, pass_turn=True)
        passes_turn(mock_event)
        actual_function.assert_not_called()

class TestSkillDecorator:
    @pytest.fixture
    def skill_component(self):
        Game()
        Game.instance.skill_system.set(Game.instance.player, SkillComponent(Game.instance.player, max_skill_points = 50))
        yield Game.instance.skill_system.get(Game.instance.player)

    def test_skill_calls_callback_when_sufficient_skill_points(self, skill_component):
        skill_component.skill_points = old_skill_points = 50
        cost = 5
        actual_function = Mock()
        mock_event = Mock()

        skill_mock = skill(actual_function, cost=cost)
        skill_mock(mock_event)

        actual_function.assert_called_with(mock_event)
        assert skill_component.skill_points == old_skill_points - cost

    def test_skill_doesnt_call_callback_when_not_sufficient_skill_points(self, skill_component):
        skill_component.skill_points = old_skill_points = 1
        cost = 50
        actual_function = Mock()
        mock_event = Mock()

        skill_mock = skill(actual_function, cost=cost)
        skill_mock(mock_event)

        actual_function.assert_not_called()
        assert skill_component.skill_points == old_skill_points
