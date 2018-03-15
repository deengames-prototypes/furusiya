from model.keys.update_manager import UpdateManager
from game import Game
import pytest
from unittest.mock import Mock, MagicMock

class TestUpdateManager:
    @pytest.fixture
    def update_man(self, monkeypatch):
        monkeypatch.setattr('model.keys.update_manager.config.data.stallion.enabled', True)
        yield UpdateManager(MagicMock())

    def test_update_takes_enemy_turns_and_restores_skill_points_if_not_player_turn(self, update_man):
        game = update_man.game
        game.current_turn = None

        update_man.update(0)

        self.test_base_update_renders_only_if_no_switching_needed(update_man)
        self.test_take_enemy_turns_takes_enemy_turns_and_switches_turns(update_man)
        self.test_restore_skill_points_restores_skill_points(update_man)

    def test_update_does_nothing_if_player_turn(self, update_man):
        game = update_man.game
        game.current_turn = game.player

        update_man.update(0)

        self.test_base_update_renders_only_if_no_switching_needed(update_man)

    def test_take_enemy_turns_takes_enemy_turns_and_switches_turns(self, update_man):
        game = update_man.game
        game.area_map.entities = [MagicMock(), MagicMock(), MagicMock()]

        update_man.take_enemy_turns()

        for e in game.area_map.entities:
            game.ai_system.take_turn.assert_any_call(e)

        assert game.current_turn == game.player

    def test_restore_skill_points_restores_skill_points(self, update_man):
        update_man.restore_skill_points()

        assert update_man.game.skill_system.get(update_man.game.player).restore_skill_points.called

    def test_base_update_renders_only_if_no_switching_needed(self, update_man):
        update_man.base_update()

        assert update_man.game.renderer.render.called

    def test_base_update_moves_to_previous_floor_when_needed(self, update_man):
        game = update_man.game
        game.renderer.recompute_fov = True
        game.area_map.previous_floor_stairs = (game.player.x, game.player.y)

        update_man.base_update()
        self.test_previous_floor_switches_to_previous_floor(update_man)

        assert game.renderer.render.called

    def test_base_update_moves_to_next_floor_when_needed(self, update_man):
        game = update_man.game
        game.renderer.recompute_fov = True
        game.area_map.next_floor_stairs = (game.player.x, game.player.y)

        update_man.base_update()
        self.test_next_floor_switches_to_next_floor(update_man)

        assert game.renderer.render.called

    def test_next_floor_switches_to_next_floor(self, update_man):
        game = update_man.game
        old_floor = game.current_floor

        update_man.next_floor()

        old_floor += 1  # needs to be augmented assignment
        assert game.current_floor == old_floor

    def test_previous_floor_switches_to_previous_floor(self, update_man):
        game = update_man.game
        old_floor = game.current_floor

        update_man.previous_floor()

        old_floor -= 1  # needs to be augmented assignment
        assert game.current_floor == old_floor

    def test_load_next_floors_area_map_removes_player_and_loads_area_map(self, update_man):
        game = update_man.game

        assert game.area_map != game.floors[game.current_floor - 1]
        old_area_map = game.area_map

        update_man.load_next_floors_area_map()

        assert game.area_map != old_area_map

        for entity in (game.player, game.stallion):
            old_area_map.entities.remove.assert_any_call(entity)

        assert game.area_map == game.floors[game.current_floor - 1]

    def test_place_player_in_floor_places_stallion_around_player_if_not_mounted(self, update_man):
        tile = 2, 2
        game = update_man.game
        game.stallion.is_mounted = False

        update_man.place_player_in_floor(tile)

        for args in ((game.player, *tile), (game.stallion, game.player.x, game.player.y)):
            game.area_map.place_around.assert_any_call(*args)

    def test_place_player_in_floor_places_stallion_on_player_if_mounted(self, update_man):
        tile = 2, 2
        game = update_man.game
        game.stallion.is_mounted = True

        update_man.place_player_in_floor(tile)

        game.area_map.place_around.assert_called_with(game.player, *tile)
        game.area_map.entities.append.assert_called_with(game.stallion)
        assert (game.stallion.x, game.stallion.y) == \
               (game.player.x, game.player.y)

    def test_place_player_in_floor_places_player_only_if_stallion_not_enabled(self, update_man, monkeypatch):
        tile = 2, 2
        game = update_man.game
        monkeypatch.setattr('model.keys.update_manager.config.data.stallion.enabled', False)

        update_man.place_player_in_floor(tile)

        game.area_map.place_around.assert_called_with(game.player, *tile)
        assert not game.entities.append.called
        with pytest.raises(AssertionError):
            game.area_map.place_around.assert_called_with(game.stallion, *tile)

    def test_refresh_renderer_resets_and_refreshes_renderer(self, update_man):
        game = update_man.game
        update_man.refresh_renderer()

        assert game.renderer.reset.called
        assert game.renderer.refresh_all.called

    def test_update_triggers_on_turn_passed_event_on_bus(self):
        g = Game()
        g.current_turn = 123 # not player, which is None
        g.events = Mock()

        u = UpdateManager(g)

        do_nothing = lambda: None
        # Stub/nullify some methods
        u.base_update = do_nothing
        u.take_enemy_turns = do_nothing
        u.restore_skill_points = do_nothing

        u.update(1)

        g.events.trigger.assert_called_with('on_turn_pass')
