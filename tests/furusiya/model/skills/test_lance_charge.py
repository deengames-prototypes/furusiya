from unittest.mock import Mock

from game import Game
from model.skills.lance_charge import LanceCharge


class TestLanceCharge:
    def test_process_deals_damage(self):
        damage = 5
        mock_fighter = Mock()
        mock_target = Mock()
        mock_config = Mock(damage=damage)

        Game.instance.fighter_system.set(mock_target, mock_fighter)

        LanceCharge.process(mock_target, mock_config)

        mock_fighter.take_damage.assert_called_with(damage)