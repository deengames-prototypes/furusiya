from furusiya.entities.player import Player
import unittest


class TestPlayer(unittest.TestCase):
    def setUp(self):
        Player.INSTANCE = None

    def tearDown(self):
        self.setUp()

    def test_player_instance_set_to_newest_player(self):
        self.assertEqual(None, Player.INSTANCE)

        p1 = Player()
        self.assertEqual(p1, Player.INSTANCE)

        p2 = Player()
        self.assertEqual(p2, Player.INSTANCE)
