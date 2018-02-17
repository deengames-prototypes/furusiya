from game import Game
from model.systems.fighter_system import FighterSystem


def target_tile(max_range=None):
    """
    return the position of a tile left-clicked in player's FOV (optionally in a range),
    or (None, None) if right-clicked.
    """
    def get_tile(event):
        if event.button == 'LEFT':
            if (event.cell in Game.renderer.visible_tiles and
                    (max_range is None or Game.player.distance(*event.cell) <= max_range)):
                return event.cell
        elif event.button == 'RIGHT':
            return None, None

    tile = None
    while tile is None:
        Game.renderer.render()
        mousedown_event = Game.ui.wait_for_mouse()
        tile = get_tile(mousedown_event)

    return tile


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
            if obj.x == x and obj.y == y and FighterSystem.get_fighter(obj) and obj != Game.player:
                return obj