import pytest

from model.gameobject import GameObject


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
