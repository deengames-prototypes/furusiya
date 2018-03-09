from game import Game
from model.config import config


def load_proper_area_map():
    Game.area_map.entities.remove(Game.player)
    if config.data.stallion.enabled:
        Game.area_map.entities.remove(Game.stallion)

    Game.area_map = Game.floors[Game.current_floor - 1]


def switch_floor_callback(tile_to_spawn_player_around):
    Game.area_map.place_around(Game.player, *tile_to_spawn_player_around)
    if config.data.stallion.enabled:
        if Game.stallion.is_mounted:
            Game.area_map.entities.append(Game.stallion)
            Game.stallion.x, Game.stallion.y = Game.player.x, Game.player.y
        else:
            Game.area_map.place_around(Game.stallion, Game.player.x, Game.player.y)
    Game.renderer.reset()
    Game.renderer.refresh_all()


def next_floor_callback():
    Game.current_floor += 1
    load_proper_area_map()
    switch_floor_callback(Game.area_map.previous_floor_stairs)


def previous_floor_callback():
    Game.current_floor -= 1
    load_proper_area_map()
    switch_floor_callback(Game.area_map.next_floor_stairs)


def base_update():
    if Game.renderer.recompute_fov:
        if (Game.player.x, Game.player.y) == Game.area_map.next_floor_stairs:
            next_floor_callback()
        elif (Game.player.x, Game.player.y) == Game.area_map.previous_floor_stairs:
            previous_floor_callback()
    Game.renderer.render()


def update_callback(delta_time):
    base_update()
    if Game.current_turn is Game.player:
        pass
    else:  # it's everyone else's turn
        enemy_turn_callback()


def enemy_turn_callback():
    for e in Game.area_map.entities:
        Game.ai_system.take_turn(e)

    Game.current_turn = Game.player

    skills = Game.skill_system.get(Game.player)
    skills.restore_skill_points(config.data.player.skillPointsPerTurn)


def quit_event(event):
    Game.save_manager.save()
    exit()


def mousemotion_event(event):
    Game.auto_target = False
    Game.mouse_coord = event.cell