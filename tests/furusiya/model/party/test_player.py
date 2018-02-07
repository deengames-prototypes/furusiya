import config
import os
import pytest

# Has to be done before other imports
path = os.path.join('furusiya', 'config.json')       
with open(path, 'rt') as f:
    raw_json = f.read()
config.load(raw_json)

from model.party.player import Player


class TestPlayer:

    def test_initializer_sets_appropriate_attributes(self):
        pass
        # print("MAKING")
        # p = Player()
        # print("MADE")
        # assert p is not None
        # print("ASSERTED {}".format(p))
