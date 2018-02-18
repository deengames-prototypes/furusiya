from unittest.mock import Mock

import pytest

from model.systems.system import ComponentSystem


@pytest.fixture()
def system():
    yield ComponentSystem()


def test_system_basic(system):
    """Tests for basic System"""
    component_1 = Mock()
    owner = Mock(id=1)

    system.set(owner, component_1)
    assert system.has(owner)
    assert system.get(owner) == component_1

    system.remove(owner)
    assert not system.has(owner)
    assert system.get(owner) is None
