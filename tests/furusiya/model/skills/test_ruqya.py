from unittest.mock import Mock

from model.skills.ruqya import Ruqya


def test_process_restores_health():
    mock_config = Mock(percent=5)
    mock_fighter = Mock(max_hp=30)

    Ruqya.process(mock_fighter, mock_config)

    assert mock_fighter.heal.called
