from unittest.mock import Mock

import pickle

import os
import pytest

from data.save_manager import SaveManager
from game import Game


class MockGame:
    _instance = None
    _dont_pickle = {'totally_not_cool_attribute'}

    def __init__(self):
        self._instance = self
        self.cool_attribute = True
        self.cooler_attribute = 9001
        self.totally_not_cool_attribute = False


class TestSaveManager:
    @pytest.fixture
    def patched_pickle(self, monkeypatch):
        m = Mock()
        monkeypatch.setattr(pickle, 'dump', m.dump)
        monkeypatch.setattr(pickle, 'load', m.load)
        yield m

    def test_save_saves_game(self, save_manager, patched_pickle):
        save_manager.save()

        assert patched_pickle.dump.called

    def test_load_loads_game(self, save_manager, patched_pickle):
        save_manager.save()
        save_manager.load()

        assert patched_pickle.load.called

    def test_load_loads_saved_game_without_raising(self):
        Game()
        save_manager = SaveManager(Game.instance)
        save_manager.save()
        save_manager.load()
        os.remove('savegame')        