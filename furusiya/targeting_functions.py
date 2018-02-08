import tdl

from main_interface import Game
from model.components.fighter import Fighter
from view.renderer import render_all


def target_monster(max_range=None):
    """
    returns a clicked monster inside FOV up to a range, or None if right-clicked
    """
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  # player cancelled
            return None

        # return the first clicked monster, otherwise continue looping
        for obj in Game.area_map.entities:
            if obj.x == x and obj.y == y and obj.get_component(Fighter) and obj != Game.player:
                return obj


def target_tile(max_range=None):
    """
    return the position of a tile left-clicked in player's FOV (optionally in a range),
    or (None, None) if right-clicked.
    """
    while True:
        # render the screen. this erases the inventory and shows the names of
        # objects under the mouse.
        tdl.flush()

        clicked = False
        for event in tdl.event.get():
            if event.type == 'MOUSEMOTION':
                Game.mouse_coord = event.cell
            if event.type == 'MOUSEDOWN' and event.button == 'LEFT':
                clicked = True
            elif ((event.type == 'MOUSEDOWN' and event.button == 'RIGHT') or
                  (event.type == 'KEYDOWN' and event.key == 'ESCAPE')):
                return None, None
        render_all()

        # accept the target if the player clicked in FOV, and in case a range is
        # specified, if it's in that range
        x = Game.mouse_coord[0]
        y = Game.mouse_coord[1]
        if (clicked and Game.mouse_coord in Game.visible_tiles and
                (max_range is None or Game.player.distance(x, y) <= max_range)):
            return Game.mouse_coord