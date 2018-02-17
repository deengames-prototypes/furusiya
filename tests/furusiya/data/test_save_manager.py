from unittest.mock import Mock

import pickle
import pytest

from data.save_manager import SaveManager


class TestSaveManager:
    @pytest.fixture
    def patched_pickle(self, monkeypatch):
        m = Mock()
        monkeypatch.setattr(pickle, 'dump', m.dump)
        monkeypatch.setattr(pickle, 'load', m.load)
        yield m

    @pytest.fixture
    def save_manager(self):
        mock_game = Mock()

        mock_game.cool_attribute.cool = True
        mock_game.cooler_attribute = 9001
        mock_game.totally_not_cool_attribute = False
        mock_game._dont_pickle = {'totally_not_cool_attribute'}

        yield SaveManager(mock_game)

    def test_save_saves_game(self, save_manager, patched_pickle):
        save_manager.save()

        assert patched_pickle.dump.called

    def test_load_loads_game(self, save_manager, patched_pickle):
        save_manager.load()

        assert patched_pickle.load.called
