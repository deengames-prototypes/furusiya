from unittest.mock import Mock

import pytest

from model.systems.system import ComponentSystem


@pytest.fixture()
def system():
    yield ComponentSystem()


def test_system_basic(system):
    """Tests for basic System"""
    component_1 = Mock()

    system.set('owner1', component_1)
    assert system.has('owner1')
    assert system.get('owner1') == component_1

    system.remove('owner1')
    assert not system.has('owner1')
    assert system.get('owner1') is None
