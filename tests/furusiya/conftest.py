import pytest

from main import init_game


@pytest.fixture(autouse=True, scope='session')
def initialize_game_for_tests():
    init_game()
