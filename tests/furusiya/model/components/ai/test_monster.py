from unittest.mock import Mock

import pytest

from game import Game
from model.components.ai.monster import BasicMonster, StunnedMonster, FrozenMonster
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


class TestFrozenMonster:
    @pytest.fixture
    def ai(self):
        mock_owner = Mock()
        Game.fighter_system.set(mock_owner, Mock())
        mock_ai = FrozenMonster(mock_owner)

        mock_ai.owner_fighter.max_hp = 1000
        yield mock_ai

    def test_take_turn_stays_stunned_for_num_turns(self, ai):
        TestStunnedMonster.test_take_turn_stays_stunned_for_num_turns(self, ai)

    def test_new_take_damage_strategy_kills_if_equal_half_health(self, ai):
        ai.owner_fighter.hp = 500

        ai.new_take_damage_strategy(50)

        assert ai.owner_fighter.die.called

    def test_new_take_damage_strategy_kills_if_below_half_health(self, ai):
        ai.owner_fighter.hp = 499

        ai.new_take_damage_strategy(50)

        assert ai.owner_fighter.die.called

    def test_new_take_damage_strategy_damages_normally_if_above_half_health(self, ai):
        ai.owner_fighter.hp = 501

        ai.new_take_damage_strategy(50)

        assert ai.owner_fighter.default_take_damage_strategy.called

    def test_cleanup_resets_attack_strategy(self, ai):
        assert ai.owner_fighter.take_damage_strategy == ai.new_take_damage_strategy
        ai.cleanup()
        assert ai.owner_fighter.take_damage_strategy == ai.owner_fighter.default_take_damage_strategy
