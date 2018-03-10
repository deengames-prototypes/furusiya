from unittest.mock import Mock

import pytest

from model.weapons import Spear


class TestSpear:
    fighter_dict = {}
    entities = []

    def _get_target(self, x, y, fighter=None):
        t = Mock(x=x, y=y)
        self.fighter_dict[t] = fighter or Mock(hostile=True)
        self.entities.append(t)
        return t

    @pytest.fixture
    def fighter(self):
        yield Mock(hostile=False)

    @pytest.fixture
    def immediate_target(self):
        yield self._get_target(x=6, y=5)

    @pytest.fixture
    def pierced_target(self):
        yield self._get_target(x=7, y=5)

    @pytest.fixture
    def not_pierced_target(self):
        yield self._get_target(x=8, y=5)

    @pytest.fixture
    def spear(self, fighter):
        owner = self._get_target(x=5, y=5, fighter=fighter)
        yield Spear(owner)

    @pytest.fixture
    def game(self):
        game = Mock()

        game.fighter_system.get.side_effect = lambda e: self.fighter_dict.get(e, Mock())
        game.fighter_system.has.return_value = True

        def get_blocking_object_at(x, y):
            objects = [
                e
                for e in self.entities
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

    def test_attack_ignores_non_hostiles(self, spear, game, fighter, immediate_target):
        for v in self.fighter_dict.values():
            v.hostile = False

        spear.attack(immediate_target, game)

        assert not fighter.attack.called

    def test_attack_pierces_enemies(self, spear, game, fighter, immediate_target, pierced_target, not_pierced_target):
        spear.attack(immediate_target, game)

        fighter.attack.assert_any_call(pierced_target, recurse=False)
        with pytest.raises(AssertionError):
            fighter.attack.assert_any_call(not_pierced_target, recurse=False)
