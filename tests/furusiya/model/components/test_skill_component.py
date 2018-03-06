import pytest

from model.components.skill import SkillComponent


class TestSkillComponent:
    @pytest.fixture
    def skill_component(self):
        from unittest.mock import Mock
        yield SkillComponent(Mock(), 50)

    def test_can_use_skill_returns_true_when_possible(self, skill_component):
        skill_component.skill_points = 50

        cost = 5
        assert skill_component.can_use_skill(cost)

        cost = 0
        assert skill_component.can_use_skill(cost)

    def test_can_use_skill_returns_false_when_not_possible(self, skill_component):
        skill_component.skill_points = 5

        cost = 50
        assert not skill_component.can_use_skill(cost)

    def test_use_skill_decreases_skill_points(self, skill_component):
        skill_component.skill_points = old_skill_points = 50
        cost = 5

        skill_component.use_skill(cost)

        assert skill_component.skill_points == old_skill_points - cost

    def test_use_skill_doesnt_result_in_negative(self, skill_component):
        skill_component.skill_points = 5
        cost = 50

        skill_component.use_skill(cost)

        assert skill_component.skill_points == 0

    def test_restore_skill_points_restores_skill_points(self, skill_component):
        skill_component.skill_points = old_skill_points = 5
        to_restore = 30

        skill_component.restore_skill_points(to_restore)

        assert skill_component.skill_points == old_skill_points + to_restore

    def test_restore_skill_points_doesnt_overflow(self, skill_component):
        skill_component.max_skill_points = 50
        skill_component.skill_points = 45
        to_restore = 30

        skill_component.restore_skill_points(to_restore)

        assert skill_component.skill_points == skill_component.max_skill_points
