import tdl

import file_watcher
from statics import SCREEN_WIDTH, SCREEN_HEIGHT, LIMIT_FPS, MAP_WIDTH, MAP_HEIGHT, PANEL_HEIGHT


class Game:
    root = None
    con = None
    panel = None
    objects = []
    inventory = []
    visible_tiles = None
    draw_bowsight = None
    player = None
    my_map = None
    fov_recompute = None
    mouse_coord = None
    auto_target = None
    target = None
    game_msgs = []
    game_state = None

    @classmethod
    def run(cls, to_run):
        tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
        cls.root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike",
                            fullscreen=False)
        tdl.setFPS(LIMIT_FPS)
        cls.con = tdl.Console(MAP_WIDTH, MAP_HEIGHT)
        cls.panel = tdl.Console(SCREEN_WIDTH, PANEL_HEIGHT)

        to_run()

        print("Terminating ...")

        file_watcher.stop()
