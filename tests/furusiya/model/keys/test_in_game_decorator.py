from unittest.mock import Mock

import pytest

from game import Game
from model.keys.in_game_decorator import in_game


@pytest.fixture(autouse=True, scope='module')
def setup_state():
    Game.game_state = 'playing'
    Game.current_turn = Game.player


def test_in_game_callback_only_calls_in_game():
    actual_function = Mock()
    mock_event = Mock()

    doesnt_pass_turn = in_game(actual_function, pass_turn=False)
    doesnt_pass_turn(mock_event)
    assert Game.current_turn is Game.player
    actual_function.assert_called_with(mock_event)

    actual_function.reset_mock()

    passes_turn = in_game(actual_function, pass_turn=True)
    passes_turn(mock_event)
    assert Game.current_turn is None
    actual_function.assert_called_with(mock_event)


def test_in_game_callback_doesnt_call_when_not_in_game():
    Game.game_state = 'dead'

    actual_function = Mock()
    mock_event = Mock()

    doesnt_pass_turn = in_game(actual_function, pass_turn=False)
    doesnt_pass_turn(mock_event)
    actual_function.assert_not_called()

    actual_function.reset_mock()

    passes_turn = in_game(actual_function, pass_turn=True)
    passes_turn(mock_event)
    actual_function.assert_not_called()


def test_in_game_callback_doesnt_call_when_not_player_turn():
    Game.current_turn = None

    actual_function = Mock()
    mock_event = Mock()

    doesnt_pass_turn = in_game(actual_function, pass_turn=False)
    doesnt_pass_turn(mock_event)
    actual_function.assert_not_called()

    actual_function.reset_mock()

    passes_turn = in_game(actual_function, pass_turn=True)
    passes_turn(mock_event)
    actual_function.assert_not_called()