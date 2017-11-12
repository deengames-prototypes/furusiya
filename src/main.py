from changquan.io.adapters.tdl_adapter import TdlAdapter
from changquan.generators.forest_generator import ForestGenerator

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

ui_adapter = TdlAdapter('Changquan Dad', SCREEN_WIDTH, SCREEN_HEIGHT)

fg = ForestGenerator(SCREEN_WIDTH, SCREEN_HEIGHT, False)
# Instead of doing this in one shot, do it in batches so we get copses of trees
total = 1/6 * SCREEN_WIDTH * SCREEN_HEIGHT

while total > 0:
    batch = min(10, total)
    total -= batch
    fg.drunken_man_walk(batch, True)


# DRAW IT!
ui_adapter.draw_walls(fg.data)