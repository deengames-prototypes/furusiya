from unittest.mock import MagicMock

import pytest

from view.targeting_monster import closest_monster


class TestClosestMonster:
    RANGE = 5

    @pytest.fixture
    def monster(self):
        yield MagicMock()

    @pytest.fixture
    def monster2(self):
        yield MagicMock()

    @pytest.fixture
    def monster3(self):
        yield MagicMock()

    @pytest.fixture
    def game(self, monster, monster2, monster3):
        game = MagicMock()

        game.area_map.entities = [monster, monster2, monster3]
        for e in game.area_map.entities:
            game.fighter_system.has(e).return_value = True
            game.fighter_system.get(e).hostile = True
            game.renderer.visible_tiles = [(e.x, e.y)]

        game.distance_dict = {
            monster: 7,
            monster2: 4,
            monster3: 1
        }

        yield game

    def test_closest_monster_ignores_non_fighters(self, game):
        game.fighter_system.has.return_value = False

        assert closest_monster(game, self.RANGE) is None

    def test_closest_monster_ignores_non_hostile_fighters(self, game):
        game.fighter_system.get().hostile = False

        assert closest_monster(game, self.RANGE) is None

    def test_closest_monster_ignores_monsters_outside_visible_tiles(self, game):
        game.renderer.visible_tiles = []

        assert closest_monster(game, self.RANGE) is None

    def test_closest_monster_ignores_monsters_outside_range(self, game):
        game.player.distance_to.return_value = 6

        assert closest_monster(game, self.RANGE) is None

    def test_closest_monster_returns_closest_monster(self, game, monster3):
        game.player.distance_to.side_effect = lambda e: game.distance_dict.get(e)

        assert closest_monster(game, self.RANGE) is monster3
