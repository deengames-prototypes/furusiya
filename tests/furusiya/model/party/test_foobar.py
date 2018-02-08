class TestFoobar:
    def test_stuff(self, config):
        x = 3
        assert x == 3
        assert config.data.features.swordStuns == True