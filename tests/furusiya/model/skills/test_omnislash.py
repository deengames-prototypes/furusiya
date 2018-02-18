from unittest.mock import Mock

import pytest

from game import Game
from model.skills.omnislash import OmniSlash


class TestOmniSlash:
    guaranteed_hits, rehit_percent = 2, 50

    @pytest.fixture
    def player(self):
        yield Mock()

    @pytest.fixture
    def player_fighter(self, player):
        fighter = Mock()
        Game.fighter_system.set(player, fighter)
        yield fighter

    @pytest.fixture
    def monster(self):
        yield Mock()

    @pytest.fixture
    def monster_fighter(self, monster):
        fighter = Mock()
        Game.fighter_system.set(monster, fighter)
        yield fighter

    @pytest.fixture
    def conf(self):
        yield Mock(guaranteedHits=self.guaranteed_hits, rehitPercent=self.rehit_percent)

    def test_slash_hits_guaranteed_hits(self, player, player_fighter, monster, monster_fighter, conf):
        # Act
        OmniSlash.process(player, monster, conf)

        # Assert
        assert player_fighter.attack.call_count >= self.guaranteed_hits

    def test_slash_hits_extra_hits(self, player, player_fighter, monster, monster_fighter, conf):
        # set random seed for deterministic extra hits
        Game.random.seed(2)
        conf.rehitPercent = 50

        # Act
        OmniSlash.process(player, monster, conf)

        # Assert
        assert player_fighter.attack.call_count >= self.guaranteed_hits + 5
