from unittest.mock import Mock

import pytest

from game import Game
from model.components.fighter import Fighter


@pytest.fixture
def fighter():
    yield Fighter(Mock(), 30, 5, 5, death_function=Mock())


@pytest.fixture
def bushslime():
    yield Mock()


@pytest.fixture
def bushslime_fighter(bushslime):
    bush_fighter = Fighter(bushslime, 15, 2, 2, death_function=Mock())
    Game.fighter_sys.set(bushslime, bush_fighter)
    yield bush_fighter


def test_take_damage(fighter):
    old_hp = fighter.hp
    fighter.take_damage(5)
    assert fighter.hp == old_hp - 5


def test_take_damage_ignore_negative(fighter):
    old_hp = fighter.hp
    fighter.take_damage(-5)
    assert fighter.hp == old_hp


def test_attack(fighter, bushslime, bushslime_fighter):
    old_hp = bushslime_fighter.hp
    fighter.attack(bushslime)
    assert bushslime_fighter.hp < old_hp


def test_attack_weapon(fighter, bushslime, bushslime_fighter):
    fighter.weapon = Mock()
    test_attack(fighter, bushslime, bushslime_fighter)
    fighter.weapon.attack.assert_called_with(bushslime)


def test_heal(fighter):
    test_take_damage(fighter)
    old_hp = fighter.hp
    fighter.heal(3)
    assert fighter.hp == old_hp + 3


def test_heal_over_max(fighter):
    test_take_damage(fighter)
    fighter.heal(fighter.max_hp)
    assert fighter.hp == fighter.max_hp


def test_take_damage_die(fighter):
    fighter.take_damage(fighter.hp)
    fighter.death_function.assert_called_with(fighter.owner)
