from unittest.mock import Mock

import pytest

from game import Game
from model.components.base import Component
from model.entities.game_object import GameObject


@pytest.fixture
def obj():
    yield GameObject(1, 1, 'j', 'test', (234, 12, 213))


class ComponentTest(Component):
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
    assert not obj.has_component(comp)

    c_instance = comp()
    obj.set_component(c_instance)

    assert obj.get_component(comp) is c_instance

    obj.remove_component(comp)

    assert not obj.has_component(comp)


def test_component_subclassed(obj, comp, subcomp1):
    subc_instance = subcomp1()
    obj.set_component(subc_instance)

    assert obj.get_component(comp) is not subc_instance
    assert obj.get_component(subcomp1) is subc_instance


def test_replace_component(obj, comp):
    obj.set_component(comp())

    new_instance = comp(10)
    obj.set_component(new_instance)

    assert obj.get_component(comp) is new_instance
    assert len(obj._components) == 1


def test_die_kills_entity(obj):
    Game.instance.area_map.entities.append(obj)

    obj.die()

    assert obj not in Game.instance.area_map.entities
    assert obj.name == ''
    assert obj.blocks is False
