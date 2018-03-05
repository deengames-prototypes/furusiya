import os
import sys
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

path_ = os.path.join(os.getcwd(), 'furusiya')
sys.path.append(path_)

import model.config.config as prod_config
from model.config import file_watcher

MonkeyPatch().setattr(file_watcher, 'watch', Mock())

with open(os.path.join(path_, 'config.json'), 'rt') as f:
    raw_json = f.read()

prod_config.load(raw_json)

from main import init_game

@pytest.fixture(scope='session', autouse=True)
def config(request):
    prod_config.data.mapType = 'dungeon'
    return prod_config


@pytest.fixture(scope='session', autouse=True)
def initialize_game_for_tests():
    init_game()
