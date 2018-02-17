class Game:
    inventory = []
    draw_bowsight = None
    player = None
    stallion = None
    mouse_coord = (0, 0)
    auto_target = None
    target = None
    game_messages = []
    game_state = None

    area_map = None
    renderer = None
    ui = None
    current_turn = None
    playing = False  # True when in-game, false otherwise

    save_load = None
    keybinder = None
