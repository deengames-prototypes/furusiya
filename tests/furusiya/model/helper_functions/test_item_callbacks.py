from unittest.mock import Mock

import pytest

from game import Game
from model.components.skill import SkillComponent
from model.config import config
from model.helper_functions.item_callbacks import restore_skill_points


class TestRestoreSkillPoints:
    @pytest.fixture()
    def skill_component(self):
        skill_component = SkillComponent(Mock(), 50)
        Game.instance.skill_system.set(Game.instance.player, skill_component)
        yield skill_component

    def test_restore_skill_points_restores_skill_points(self, skill_component):
        config.data.item.skillPointPotion.restores = to_restore = 15
        skill_component.max_skill_points = 50
        skill_component.skill_points = old_skill_points = 30

        restore_skill_points()

        assert skill_component.skill_points == old_skill_points + to_restore

    def test_restore_skill_points_doesnt_overflow(self, skill_component):
        skill_component.max_skill_points = 50
        config.data.item.skillPointPotion.restores = 15
        skill_component.skill_points = 40

        restore_skill_points()

        assert skill_component.skill_points == skill_component.max_skill_points

    def test_restore_skill_points_doesnt_restore_if_full(self, skill_component):
        skill_component.max_skill_points = skill_component.skill_points = 50

        restore_skill_points()

        assert skill_component.skill_points == skill_component.max_skill_points
