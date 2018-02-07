from unittest.mock import Mock

import pytest

from model.components.base import Component
from model.game_object import GameObject


@pytest.fixture
def obj():
    yield GameObject(1, 1, 'j', 'test', (234, 12, 213))


class ComponentTest(Component):
    component_type = 'Type1'

    def __init__(self, owner=Mock(), value=0):
        super().__init__(owner)
        self.value = value


class SubComponentTest1(ComponentTest):
    pass


class SubComponentTest2(ComponentTest):
    pass


@pytest.fixture
def comp():
    yield ComponentTest


@pytest.fixture
def subcomp1():
    yield SubComponentTest1


@pytest.fixture
def subcomp2():
    yield SubComponentTest2


def test_basic(obj, comp):
    assert obj.get_component(comp) is None

    c_instance = comp()
    obj.set_component(c_instance)

    assert obj.get_component(comp) is c_instance

    obj.remove_component(comp)

    assert obj.get_component(comp) is None


def test_component_subclassed(obj, comp, subcomp1):
    subc_instance = subcomp1()
    obj.set_component(subc_instance)

    assert obj.get_component(comp) is subc_instance


def test_replace_component(obj, comp):
    obj.set_component(comp())

    new_instance = comp(10)
    obj.set_component(new_instance)

    assert obj.get_component(comp) is new_instance
    assert len(obj._components) == 1


def test_replace_subcomponent(obj, comp, subcomp1, subcomp2):
    original = subcomp1(value=1)
    obj.set_component(original)
    assert obj.get_component(comp) == original

    replacer = subcomp2(value=2)
    obj.set_component(replacer)

    assert obj.get_component(comp) == replacer
    assert obj.get_component(comp) != original
    assert len(obj._components) == 1
