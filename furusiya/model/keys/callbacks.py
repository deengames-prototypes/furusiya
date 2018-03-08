from game import Game
from model.config import config


def next_floor_callback():
    Game.current_floor += 1

    Game.area_map.entities.remove(Game.player)
    if config.data.stallion.enabled:
        Game.area_map.entities.remove(Game.stallion)

    Game.area_map = Game.floors[Game.current_floor - 1]

    Game.area_map.place_on_random_ground(Game.player)
    if config.data.stallion.enabled:
        if Game.stallion.is_mounted:
            Game.area_map.entities.append(Game.stallion)
            Game.stallion.x, Game.stallion.y = Game.player.x, Game.player.y
        else:
            Game.area_map.place_around(Game.stallion, Game.player.x, Game.player.y)

    Game.renderer._area_map = Game.area_map
    Game.renderer.recompute_fov = True
    Game.renderer._all_tiles_rendered = False
    Game.renderer.visible_tiles = []
    Game.renderer.refresh_all()


def base_update():
    Game.renderer.render()
    if (Game.player.x, Game.player.y) == Game.area_map.stairs:
        next_floor_callback()


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