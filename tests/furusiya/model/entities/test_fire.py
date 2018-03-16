from game import Game
from model.config import config
from model.entities.fire import Fire
from model.event.event_bus import EventBus
import pytest
from unittest.mock import Mock, MagicMock


def setup_module(module):
    Game()
    Game.instance.event_bus = EventBus()
    Game.instance.ui = Mock()

class TestFire:
    @pytest.fixture
    def fire(self):
        yield Fire(2, 2)

    @pytest.fixture
    def fighter(self):
        yield Mock()

    @pytest.fixture
    def entity(self, fighter):
        e = Mock()
        Game.instance.fighter_system.set(e, fighter)
        yield e

    @pytest.fixture(autouse=True, scope='class')
    def game(self):
        old_map = Game.instance.area_map
        Game.instance.area_map = MagicMock()
        Game.instance.area_map.mutate_position_if_walkable.side_effect = lambda x, y: (x + 1, y)
        yield
        Game.instance.area_map = old_map

    def test_on_entity_move_damages_entity_and_extinguishes_self(self, fire, entity, fighter):
        fire.cleanup = Mock()
        entity.x, entity.y = fire.x, fire.y
        fighter.defense = 1

        fire.on_entity_move(entity)

        assert fighter.take_damage.called
        assert fire.cleanup.called

    def test_on_entity_move_ignores_entity_if_not_same_pos(self, fire, entity, fighter):
        fire.cleanup = Mock()

        fire.on_entity_move(entity)

        assert not fighter.take_damage.called
        assert not fire.cleanup.called

    def test_on_turn_passed_auto_extinguishes_after_num_turns(self, fire):
        fire.cleanup = Mock()

        for _ in range(config.data.enemies.fire.selfExtinguishTurns):
            assert not fire.cleanup.called
            fire.on_turn_passed()

        assert fire.cleanup.called

    def test_on_turn_passed_spreads_to_nearby_tiles(self, fire, monkeypatch):
        Game.instance.area_map.reset_mock()
        monkeypatch.setattr(Game.instance.random, 'randint', Mock(return_value=config.data.enemies.fire.spreadProbability))
        Game.instance.area_map.get_entities_on.return_value = []

        def append(e):
            assert fire.x == e.x or fire.y == e.y

        Game.instance.area_map.entities.append.side_effect = append

        fire.on_turn_passed()

        assert Game.instance.area_map.entities.append.called

    def test_on_turn_passed_doesnt_spread_if_already_burning(self, fire, monkeypatch):
        Game.instance.area_map.reset_mock()
        monkeypatch.setattr(Game.instance.random, 'randint', Mock(return_value=config.data.enemies.fire.spreadProbability))
        Game.instance.area_map.get_entities_on.return_value = [Fire(fire.x, fire.y)]

        fire.on_turn_passed()

        assert not Game.instance.area_map.entities.append.called

    def test_on_turn_passed_immediately_destroys_non_fighter_entities_spread_upon(self, fire,  monkeypatch):
        Game.instance.area_map.reset_mock()
        monkeypatch.setattr(Game.instance.random, 'randint', Mock(return_value=config.data.enemies.fire.spreadProbability))

        entity = Mock(x=fire.x, y=fire.y)
        Game.instance.area_map.get_entities_on.return_value = [entity]
        fire.default_death_function = Mock()

        fire.on_turn_passed()

        assert entity.default_death_function.called

    def test_on_turn_passed_immediately_damages_fighter_entities_spread_upon(self, fire,  monkeypatch):
        Game.instance.area_map.reset_mock()
        monkeypatch.setattr(Game.instance.random, 'randint', Mock(return_value=config.data.enemies.fire.spreadProbability))

        entity = Mock(x=fire.x, y=fire.y)
        Game.instance.area_map.get_entities_on.return_value = [entity]
        fire.default_death_function = Mock()

        fighter = Mock(defense=1)
        Game.instance.fighter_system.set(entity, fighter)

        fire.on_turn_passed()

        assert fighter.take_damage.called
