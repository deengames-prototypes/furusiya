from game import Game
from model.entities.party.player import Player
from model.skills.omnislash import OmniSlash
import pytest
import random
from unittest.mock import Mock

class TestOmniSlash:
    guaranteed_hits, rehit_percent = 2, 50


    @pytest.fixture
    def player_fighter(self, player):
        fighter = Mock()
        Game.instance.fighter_system.set(player, fighter)
        Game.instance.player = player
        yield fighter

    @pytest.fixture
    def monster(self):
        yield Mock()

    @pytest.fixture
    def monster_fighter(self, monster):
        fighter = Mock()
        Game.instance.fighter_system.set(monster, fighter)
        yield fighter

    @pytest.fixture
    def conf(self):
        yield Mock(guaranteedHits=self.guaranteed_hits, probabilityOfAnotherHit=self.rehit_percent)

    def test_slash_hits_guaranteed_hits(self, player, player_fighter, monster, monster_fighter, conf):
        for _ in range(10):
            # Act
            OmniSlash.process(player, monster, conf)

            # Assert
            assert player_fighter.attack.call_count >= self.guaranteed_hits

            # Clean up
            player_fighter.reset_mock()

    def test_slash_hits_extra_hits(self, player, player_fighter, monster, monster_fighter, conf):
        Game()
        Game.instance.random = random.Random()
        # set random seed for deterministic extra hits
        Game.instance.random.seed(2)
        conf.probabilityOfAnotherHit = 50

        # Act
        OmniSlash.process(player, monster, conf)

        # Assert
        assert player_fighter.attack.call_count > self.guaranteed_hits
