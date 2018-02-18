import os
import sys

import pytest

path_ = os.path.join(os.getcwd(), 'furusiya')
sys.path.append(path_)

import model.config.config as prod_config
from main import init_game

with open(os.path.join(path_, 'config.json'), 'rt') as f:
    raw_json = f.read()

prod_config.load(raw_json)


@pytest.fixture(scope='session', autouse=True)
def config(request):
    prod_config.data.mapType = 'dungeon'
    return prod_config


@pytest.fixture(autouse=True, scope='session')
def initialize_game_for_tests():
    init_game()
