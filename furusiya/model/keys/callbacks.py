from game import Game


def quit_event(event):
    Game.save_manager.save()
    exit()


def mousemotion_event(event):
    Game.auto_target = False
    Game.mouse_coord = event.cell