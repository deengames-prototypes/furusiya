from unittest.mock import Mock

import pytest

from model.weapons import Spear


class TestSpear:
    fighter_dict = {}

    @pytest.fixture
    def fighter(self):
        yield Mock(hostile=False)

    @pytest.fixture
    def immediate_target(self):
        yield Mock(x=6, y=5)

    @pytest.fixture
    def pierced_target(self):
        yield Mock(x=7, y=5)

    @pytest.fixture
    def spear(self):
        yield Spear(Mock(x=5, y=5))

    @pytest.fixture
    def game(self, spear, fighter, immediate_target, pierced_target):
        game = Mock()

        self.fighter_dict.update({
            spear.owner: fighter,
            immediate_target: Mock(hostile=True),
            pierced_target: Mock(hostile=True)
        })

        game.fighter_system.get.side_effect = lambda e: self.fighter_dict.get(e, Mock())
        game.fighter_system.has.return_value = True

        entities = [spear.owner, immediate_target, pierced_target]

        def get_blocking_object_at(x, y):
            objects = [
                e
                for e in entities
                if (e.x, e.y) == (x, y)
            ]
            if len(objects) == 0:
                return None
            else:
                return objects[0]

        game.area_map.get_blocking_object_at.side_effect = get_blocking_object_at

        yield game

    def test_attack_ignores_empty_tiles(self, spear, game, fighter, immediate_target):
        game.area_map.get_blocking_object_at = lambda x, y: None

        spear.attack(immediate_target, game)

        assert not fighter.attack.called

    def test_attack_ignores_target(self, spear, game, fighter, immediate_target):
        game.area_map.get_blocking_object_at = lambda x, y: immediate_target

        spear.attack(immediate_target, game)

        assert not fighter.attack.called

    def test_attack_ignores_non_fighters(self, spear, game, fighter, immediate_target):
        game.fighter_system.has.return_value = False

        spear.attack(immediate_target, game)

        assert not fighter.attack.called

    def test_attack_ignores_non_hostiles(self, spear, game, fighter, immediate_target, pierced_target):
        self.fighter_dict[immediate_target].hostile = False
        self.fighter_dict[pierced_target].hostile = False

        spear.attack(immediate_target, game)

        assert not fighter.attack.called

    def test_attack_pierces_enemies(self, spear, game, fighter, immediate_target, pierced_target):
        spear.attack(immediate_target, game)

        fighter.attack.assert_any_call(pierced_target, recurse=False)
