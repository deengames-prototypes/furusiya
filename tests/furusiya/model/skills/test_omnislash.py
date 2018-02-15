from unittest.mock import Mock

from model.skills.omnislash import OmniSlash


def test_process():
    player = Mock()

    for _ in range(100):
        OmniSlash.process(player, 10, (1, 0))

    assert 20 > player.move_or_attack.call_count > 5  # Roughly estimate. Yay randomness!
