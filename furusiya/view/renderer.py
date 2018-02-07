import tdl

import colors
import config
from constants import FOV_ALGO, FOV_LIGHT_WALLS, MAP_HEIGHT, MAP_WIDTH, color_dark_wall, color_dark_ground, \
    color_light_wall, color_light_ground, MSG_X, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT
from main_interface import Game
from model.components.fighter import Fighter


def render_all():
    if Game.fov_recompute:
        Game.fov_recompute = False
        Game.visible_tiles = tdl.map.quickFOV(Game.player.x, Game.player.y,
                                              is_visible_tile,
                                              fov=FOV_ALGO,
                                              radius=config.data.player.lightRadius,
                                              lightWalls=FOV_LIGHT_WALLS)

        # go through all tiles, and set their background color according to the FOV
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = (x, y) in Game.visible_tiles
                wall = Game.area_map.tiles[x][y].block_sight
                if not visible:
                    # if it's not visible right now, the player can only see it
                    # if it's explored
                    if Game.area_map.tiles[x][y].is_explored:
                        if wall:
                            Game.con.draw_char(x, y, '#', fg=color_dark_wall)
                        else:
                            Game.con.draw_char(x, y, '.', fg=color_dark_ground)
                elif not Game.draw_bowsight:
                    if wall:
                        Game.con.draw_char(x, y, '#', fg=color_light_wall)
                    else:
                        Game.con.draw_char(x, y, '.', fg=color_light_ground)
                    # since it's visible, explore it
                    Game.area_map.tiles[x][y].is_explored = True

    if Game.draw_bowsight:
        # Horrible, terrible, crazy hack. Can't figure out why visible tiles
        # just never seem to redraw as '.' or '#' on top of bow rays.
        for (x, y) in Game.visible_tiles:
            char = '#' if Game.area_map.tiles[x][y].block_sight else '.'
            Game.con.draw_char(x, y, char, fg=color_light_ground)

        if Game.auto_target:
            Game.target = closest_monster(config.data.player.lightRadius)
            x2, y2 = (Game.target.x, Game.target.y) if Game.target is not None else Game.mouse_coord
        else:
            Game.target = None
            x2, y2 = Game.mouse_coord
        x1, y1 = Game.player.x, Game.player.y
        line = tdl.map.bresenham(x1, y1, x2, y2)
        for pos in line:
            Game.con.draw_char(pos[0], pos[1], '*', colors.dark_green, bg=None)
        tdl.flush()

        # Undo drawing tiles outside sight
        for pos in line:
            if not pos in Game.visible_tiles:
                Game.con.draw_char(pos[0], pos[1], '#', colors.black)

    # draw all objects in the list
    for obj in Game.area_map.entities:
        if obj != Game.player:
            if Game.draw_bowsight and (obj.x, obj.y) in Game.visible_tiles and \
                            (obj.x, obj.y) == (x2, y2) and obj.get_component(Fighter) is not None:
                Game.target = obj
                Game.con.draw_char(obj.x, obj.y, 'X', fg=colors.red)
            else:
                obj.draw()

    Game.player.draw()
    Game.stallion.draw()

    # blit the contents of "Game.con" to the root console and present it
    Game.root.blit(Game.con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0)

    # prepare to render the GUI Game.panel
    Game.panel.clear(fg=colors.white, bg=colors.black)

    # print the game messages, one line at a time
    y = 1
    for (line, color) in Game.game_msgs:
        Game.panel.draw_str(MSG_X, y, line, bg=None, fg=color)
        y += 1

    # show the player's stats
    player_fighter = Game.player.get_component(Fighter)
    Game.panel.draw_str(1, 1, "HP: {}/{}".format(player_fighter.hp, player_fighter.max_hp))
    # render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp,
    #     colors.light_red, colors.darker_red)

    # display names of objects under the mouse
    Game.panel.draw_str(1, 0, get_names_under_mouse(), bg=None, fg=colors.light_gray)

    # blit the contents of "Game.panel" to the root console
    Game.root.blit(Game.panel, 0, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0)

    tdl.flush()


def is_visible_tile(x, y):

    if x >= MAP_WIDTH or x < 0:
        return False
    elif y >= MAP_HEIGHT or y < 0:
        return False
    elif not Game.area_map.tiles[x][y].is_walkable:
        return False
    elif Game.area_map.tiles[x][y].block_sight:
        return False
    else:
        return True


def get_names_under_mouse():
    # create a list with the names of all objects at the mouse's coordinates and in FOV
    names = [obj.name for obj in get_objects_under_mouse()]

    names = ', '.join(names)  # join the names, separated by commas
    return names.capitalize()


def get_objects_under_mouse():
    (x, y) = Game.mouse_coord

    # create a list with the names of all objects at the mouse's coordinates and in FOV
    stuff = [obj for obj in Game.area_map.entities
             if obj.x == x and obj.y == y and (obj.x, obj.y) in Game.visible_tiles]

    return stuff


def closest_monster(max_range):
    # find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  # start with (slightly more than) maximum range

    for obj in Game.area_map.entities:
        if obj.get_component(Fighter) and not obj == Game.player and (obj.x, obj.y) in Game.visible_tiles:
            # calculate distance between this object and the player
            dist = Game.player.distance_to(obj)
            if dist < closest_dist:  # it's closer, so remember it
                closest_enemy = obj
                closest_dist = dist
    return closest_enemy