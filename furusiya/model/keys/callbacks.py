from game import Game
from model.config import config


def update_callback(delta_time):
    Game.renderer.render()
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