from main_interface import Game
from model.components.fighter import Fighter


def closest_monster(max_range):
    # find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  # start with (slightly more than) maximum range

    for obj in Game.area_map.entities:
        if obj.get_component(Fighter) and not obj == Game.player and (obj.x, obj.y) in Game.renderer.visible_tiles:
            # calculate distance between this object and the player
            dist = Game.player.distance_to(obj)
            if dist < closest_dist:  # it's closer, so remember it
                closest_enemy = obj
                closest_dist = dist
    return closest_enemy