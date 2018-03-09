from unittest.mock import Mock

import pytest

from game import Game
from model.components.ai.monster import BasicMonster, StunnedMonster
from model.config import config


class TestBasicMonster:
    @pytest.fixture
    def ai(self):
        mock_ai = BasicMonster(Mock())

        visible_tile = (1, 1)
        Game.renderer = Mock(visible_tiles=[visible_tile])
        mock_ai.owner.x, mock_ai.owner.y = visible_tile

        Game.fighter_system.set(Game.player, Mock(hp=5))
        Game.fighter_system.set(mock_ai.owner, Mock())

        yield mock_ai

    def test_take_turn_moves_towards_player_when_in_sight(self, ai):
        ai.owner.distance_to.return_value = 4

        ai.take_turn()

        assert ai.owner.move_towards.called

    def test_take_turn_attacks_player_when_close_enough(self, ai):
        ai.owner.distance_to.return_value = 1

        ai.take_turn()

        Game.fighter_system.get(ai.owner).attack.assert_called_with(Game.player)

    if config.data.enemies.randomlyWalkWhenOutOfSight:
        def test_take_turn_randomly_walks_if_out_of_sight(self, ai, monkeypatch):
            Game.renderer.visible_tiles = []
            mock_walker = Mock()
            monkeypatch.setattr('model.components.ai.monster.RandomWalker', mock_walker)

            ai.take_turn()

            assert mock_walker.called
            assert mock_walker().walk.called


class TestStunnedMonster:
    @pytest.fixture
    def ai(self):
        yield StunnedMonster(Mock())

    def test_take_turn_stays_stunned_for_num_turns(self, ai):
        ai.num_turns = num_turns = 5
        ai.owner.name = 'tiger'

        for i in range(num_turns, 1, -1):
            old_num_turns = ai.num_turns
            ai.take_turn()
            assert ai.owner.char == str(i-1)[-1]
            assert ai.num_turns == old_num_turns - 1

        ai.take_turn()
        assert ai.num_turns == 0
        assert ai.owner.char == 't'
