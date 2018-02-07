import pytest

from model.game_object import GameObject


@pytest.fixture
def obj():
    yield GameObject(1, 1, 'j', 'test', (234, 12, 213))


class TestComp:
    def __init__(self, value=0):
        self.value = value


class TestSubComp(TestComp):
    pass


@pytest.fixture
def comp():
    yield TestComp


@pytest.fixture
def subcomp():
    yield TestSubComp


def test_basic(obj, comp):
    assert obj.get_component(comp) is None

    c_instance = comp()
    obj.set_component(c_instance)

    assert obj.get_component(comp) is c_instance

    obj.del_component(comp)

    assert obj.get_component(comp) is None


def test_component_subclassed(obj, comp, subcomp):
    subc_instance = subcomp()
    obj.set_component(subc_instance)

    assert obj.get_component(comp) is subc_instance


def test_replace_component(obj, comp):
    obj.set_component(comp())

    new_instance = comp(10)
    obj.set_component(new_instance)

    assert obj.get_component(comp) is new_instance
    assert len(obj._components) == 1
