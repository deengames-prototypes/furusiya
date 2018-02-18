from unittest.mock import Mock

import pytest

from game import Game
from model.components.fighter import Fighter


class TestFighter:
    @pytest.fixture
    def fighter(self, ):
        yield Fighter(Mock(), 30, 5, 5, death_function=Mock())

    @pytest.fixture
    def bushslime(self, ):
        yield Mock()

    @pytest.fixture
    def bushslime_fighter(self, bushslime):
        bush_fighter = Fighter(bushslime, 15, 2, 2, death_function=Mock())
        Game.fighter_sys.set(bushslime, bush_fighter)
        yield bush_fighter

    def test_take_damage_decreases_health(self, fighter):
        health_to_decrease = 5
        old_hp = fighter.hp

        # Act
        fighter.take_damage(health_to_decrease)

        # Assert
        assert fighter.hp == old_hp - health_to_decrease

    def test_take_damage_ignore_negative_damage(self, fighter):
        old_hp = fighter.hp

        # Act
        fighter.take_damage(-5)

        # Assert
        assert fighter.hp == old_hp

    def test_attack_decreases_damage(self, fighter, bushslime, bushslime_fighter):
        old_hp = bushslime_fighter.hp

        # Act
        fighter.attack(bushslime)

        # Assert
        assert bushslime_fighter.hp < old_hp

    def test_attack_attacks_with_weapon_effect(self, fighter, bushslime, bushslime_fighter):
        fighter.weapon = Mock()

        # Act
        fighter.attack(bushslime)

        # Assert
        fighter.weapon.attack.assert_called_with(bushslime)

    def test_heal_increases_health(self, fighter):
        self.test_take_damage_decreases_health(fighter)
        expected_health_gain = 3
        old_hp = fighter.hp

        # Act
        fighter.heal(expected_health_gain)

        # Assert
        assert fighter.hp == old_hp + expected_health_gain

    def test_heal_overhealing_heals_to_max(self, fighter):
        self.test_take_damage_decreases_health(fighter)

        # Act
        fighter.heal(fighter.max_hp)

        # Assert
        assert fighter.hp == fighter.max_hp

    def test_take_damage_kills_entity_if_out_of_health(self, fighter):
        # Act
        fighter.take_damage(fighter.hp)

        # Assert
        fighter.death_function.assert_called_with(fighter.owner)
