from main_interface import Game
from model.systems.fighter_system import FighterSystem


def target_tile(max_range=None):
    """
    return the position of a tile left-clicked in player's FOV (optionally in a range),
    or (None, None) if right-clicked.
    """
    # TODO: This basically pauses the core game loop and starts this one.
    # This definitely needs to be cleaned up.
    while True:
        # render the screen. this erases the inventory and shows the names of
        # objects under the mouse.
        Game.ui.flush()

        clicked = False
        user_input = Game.ui.get_input()

        if user_input.type == 'MOUSEMOTION':
            Game.mouse_coord = user_input.cell
        if user_input.type == 'MOUSEDOWN' and user_input.button == 'LEFT':
            clicked = True
        elif ((user_input.type == 'MOUSEDOWN' and user_input.button == 'RIGHT') or
              (user_input.type == 'KEYDOWN' and user_input.key == 'ESCAPE')):
            return None, None

        Game.renderer.render()

        # accept the target if the player clicked in FOV, and in case a range is
        # specified, if it's in that range
        x = Game.mouse_coord[0]
        y = Game.mouse_coord[1]
        if (clicked and Game.mouse_coord in Game.renderer.visible_tiles and
                (max_range is None or Game.player.distance(x, y) <= max_range)):
            return Game.mouse_coord


def target_monster(max_range=None):
    """
    returns a clicked monster inside FOV up to a range, or None if right-clicked
    """
    # TODO: Same as target_tile :/
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  # player cancelled
            return None

        # return the first clicked monster, otherwise continue looping
        for obj in Game.area_map.entities:
            if obj.x == x and obj.y == y and FighterSystem.get_fighter(obj) and obj != Game.player:
                return obj