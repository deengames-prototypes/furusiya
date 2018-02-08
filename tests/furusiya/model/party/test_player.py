from model.entities.party.player import Player


class TestPlayer:

    def test_initializer_sets_appropriate_attributes(self, config):
        assert config.data.features.swordStuns == True
        pass
        # print("MAKING")
        # p = Player()
        # print("MADE")
        # assert p is not None
        # print("ASSERTED {}".format(p))
