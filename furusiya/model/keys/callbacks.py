from game import Game
from model.config import config


class UpdateManager:
    def __init__(self, game):
        self.game = game

    def load_next_floors_area_map(self):
        self.game.area_map.entities.remove(self.game.player)
        if config.data.stallion.enabled:
            self.game.area_map.entities.remove(self.game.stallion)

        self.game.area_map = self.game.floors[self.game.current_floor - 1]

    def place_player_in_floor(self, tile_to_spawn_player_around):
        self.game.area_map.place_around(self.game.player, *tile_to_spawn_player_around)
        if config.data.stallion.enabled:
            if self.game.stallion.is_mounted:
                self.game.area_map.entities.append(self.game.stallion)
                self.game.stallion.x, self.game.stallion.y = self.game.player.x, self.game.player.y
            else:
                self.game.area_map.place_around(self.game.stallion, self.game.player.x, self.game.player.y)

    def refresh_renderer(self):
        self.game.renderer.reset()
        self.game.renderer.refresh_all()

    def next_floor(self):
        self.game.current_floor += 1
        self.load_next_floors_area_map()
        self.place_player_in_floor(self.game.area_map.previous_floor_stairs)
        self.refresh_renderer()

    def previous_floor(self):
        self.game.current_floor -= 1
        self.load_next_floors_area_map()
        self.place_player_in_floor(self.game.area_map.next_floor_stairs)
        self.refresh_renderer()

    def base_update(self):
        if self.game.renderer.recompute_fov:
            if (self.game.player.x, self.game.player.y) == self.game.area_map.next_floor_stairs:
                self.next_floor()
            elif (self.game.player.x, self.game.player.y) == self.game.area_map.previous_floor_stairs:
                self.previous_floor()
        self.game.renderer.render()

    def update(self, delta_time):
        self.base_update()
        if self.game.current_turn is self.game.player:
            pass
        else:  # it's everyone else's turn
            self.take_enemy_turns()

    def take_enemy_turns(self):
        for e in self.game.area_map.entities:
            self.game.ai_system.take_turn(e)

        self.game.current_turn = self.game.player

        skills = self.game.skill_system.get(self.game.player)
        skills.restore_skill_points(config.data.player.skillPointsPerTurn)


def quit_event(event):
    Game.save_manager.save()
    exit()


def mousemotion_event(event):
    Game.auto_target = False
    Game.mouse_coord = event.cell