from unittest.mock import Mock

import pytest

from model.weapons import Spear


class TestSpear:
    fighter_dict = {}

    @pytest.fixture
    def fighter(self):
        yield Mock(hostile=False)

    @pytest.fixture
    def target(self):
        yield Mock(x=6, y=5)

    @pytest.fixture
    def target2(self):
        yield Mock(x=7, y=5)

    @pytest.fixture
    def spear(self):
        yield Spear(Mock(x=5, y=5))

    @pytest.fixture
    def game(self, spear, fighter, target, target2):
        game = Mock()

        self.fighter_dict.update({
            spear.owner: fighter,
            target: Mock(hostile=True),
            target2: Mock(hostile=True)
        })

        game.fighter_system.get.side_effect = lambda e: self.fighter_dict.get(e, Mock())
        game.fighter_system.has.return_value = True

        entities = [spear.owner, target, target2]

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

    def test_attack_ignores_empty_tiles(self, spear, game, fighter, target):
        game.area_map.get_blocking_object_at = lambda x, y: None

        spear.attack(target, game)

        assert not fighter.attack.called

    def test_attack_ignores_target(self, spear, game, fighter, target):
        game.area_map.get_blocking_object_at = lambda x, y: target

        spear.attack(target, game)

        assert not fighter.attack.called

    def test_attack_ignores_non_fighters(self, spear, game, fighter, target):
        game.fighter_system.has.return_value = False

        spear.attack(target, game)

        assert not fighter.attack.called

    def test_attack_ignores_non_hostiles(self, spear, game, fighter, target, target2):
        self.fighter_dict[target].hostile = False
        self.fighter_dict[target2].hostile = False

        spear.attack(target, game)

        assert not fighter.attack.called

    def test_attack_pierces_enemies(self, spear, game, fighter, target, target2):
        spear.attack(target, game)

        fighter.attack.assert_any_call(target2, recurse=False)
