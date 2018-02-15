from unittest.mock import Mock

import pytest

from model.systems.system import System


@pytest.fixture()
def system():
    yield System('DummySystem', (), {'_component_name': 'component'})


def test_system_basic(system):
    """Tests for basic System metaclass"""
    component_1 = Mock()

    system.set_component('owner1', component_1)
    assert system.has_component('owner1')
    assert system.get_component('owner1') == component_1

    system.remove_component('owner1')
    assert not system.has_component('owner1')
    assert system.get_component('owner1') is None
