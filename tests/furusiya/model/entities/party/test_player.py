import pytest

from model.entities.party.player import Player
from model.config import config


class TestPlayer:
    @pytest.fixture
    def player(self):
        yield Player()

    def test_can_use_skill_returns_true_when_possible(self, player):
        player.skill_points = 50

        cost = 5
        assert player.can_use_skill(cost)

        cost = 0
        assert player.can_use_skill(cost)

    def test_can_use_skill_returns_false_when_not_possible(self, player):
        player.skill_points = 5

        cost = 50
        assert not player.can_use_skill(cost)

    def test_use_skill_decreases_skill_points(self, player):
        player.skill_points = old_skill_points = 50
        cost = 5

        player.use_skill(cost)

        assert player.skill_points == old_skill_points - cost

    def test_use_skill_doesnt_result_in_negative(self, player):
        player.skill_points = 5
        cost = 50

        player.use_skill(cost)

        assert player.skill_points == 0

    def test_restore_skill_points_restores_skill_points(self, player):
        player.skill_points = old_skill_points = 5
        to_restore = 30

        player.restore_skill_points(to_restore)

        assert player.skill_points == old_skill_points + to_restore

    def test_restore_skill_points_doesnt_overflow(self, player):
        config.data.player.maxSkillPoints = 50
        player.skill_points = 45
        to_restore = 30

        player.restore_skill_points(to_restore)

        assert player.skill_points == config.data.player.maxSkillPoints
