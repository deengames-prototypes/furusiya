from game import Game
from model.keys.key_callbacks import exit_to_main_menu_callback
from model.systems.ai_system import AISystem


def update_callback(delta_time):
    Game.renderer.render()
    if Game.current_turn is Game.player:
        pass
    else:  # it's everyone else's turn
        for e in Game.area_map.entities:
            AISystem.take_turn(e)

        Game.current_turn = Game.player


def quit_event(event):
    exit_to_main_menu_callback(event)
    exit()


def mousemotion_event(event):
    Game.auto_target = False
    Game.mouse_coord = event.cell