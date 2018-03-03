import pytest

from game import Game
from model.config import config
from model.helper_functions.item_callbacks import restore_skill_points


class TestRestoreSkillPoints:
    @pytest.fixture()
    def player(self):
        yield Game.player

    def test_restore_skill_points_restores_skill_points(self, player):
        config.data.player.maxSkillPoints = 50
        config.data.item.skillPointPotion.restores = to_restore = 15
        player.skill_points = old_skill_points = 30

        restore_skill_points()

        assert player.skill_points == old_skill_points + to_restore

    def test_restore_skill_points_doesnt_overflow(self, player):
        config.data.player.maxSkillPoints = max_skill_points = 50
        config.data.item.skillPointPotion.restores = 15
        player.skill_points = 40

        restore_skill_points()

        assert player.skill_points == max_skill_points

    def test_restore_skill_points_doesnt_restore_if_full(self, player):
        config.data.player.maxSkillPoints = max_skill_points = player.skill_points = 50

        restore_skill_points()

        assert player.skill_points == max_skill_points
