from game import Game
from model.components.xp import XPComponent
from model.maps.area_map import AreaMap
from model.entities.game_object import GameObject
from model.entities.party.player import Player
from model.helper_functions.death_functions import monster_death, player_death, horse_death
import pytest
from unittest.mock import Mock

MONSTER_XP = 50

@pytest.fixture
def monster():
    obj = GameObject(2, 2, 's', 'scary monster', (0, 0, 0), blocks=True)

    Game.instance.xp_system.set(obj, Mock(xp=MONSTER_XP))
    Game.instance.fighter_system.set(obj, Mock())
    Game.instance.ai_system.set(obj, Mock())

    yield obj


@pytest.fixture
def player():
    Game.instance.xp_system.set(Game.instance.player, XPComponent(Game.instance.player))
    Game.instance.keybinder = Mock()

    yield Game.instance.player


def test_monster_death_marks_monster_as_dead(monster, player):
    Game()
    Game.instance.player = player
    player_xp = Game.instance.xp_system.get(player)
    old_xp = player_xp.xp

    monster_death(monster)
    new_xp = player_xp.xp

    assert monster.char == '%'
    assert monster.blocks is False

    assert new_xp > old_xp

    assert not Game.instance.fighter_system.has(monster)
    assert not Game.instance.ai_system.has(monster)


def test_player_death_affects_game_state(player):
    Game()
    Game.instance.player = player
    Game.instance.game_state = 'playing'

    player_death(player)

    assert Game.instance.game_state == 'dead'
    assert player.char == '%'


def test_horse_death_removes_components(monster):
    Game()
    Game.instance.player = Player()
    Game.instance.area_map = AreaMap(10, 10)
    horse_death(monster)

    assert monster.char == '%'
    assert monster.blocks is False

    assert not Game.instance.fighter_system.has(monster)
    assert not Game.instance.ai_system.has(monster)