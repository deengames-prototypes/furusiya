import random
import shelve
from random import randint

import tdl

import colors
import config
from constants import *
from main_interface import Game, menu, message
from model.components.ai.base import AI
from model.components.ai.monster import ConfusedMonster
from model.components.fighter import Fighter
from model.factories import monster_factory, item_factory
from model.item import Item
from model.party.player import Player
from model.party.stallion import Stallion
from model.rect import Rect
from model.tile import Tile
from model.weapons import Bow


def create_room(room):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            Game.area_map.tiles[x][y].is_walkable = True
            Game.area_map.tiles[x][y].block_sight = False


def create_h_tunnel(x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        Game.area_map.tiles[x][y].is_walkable = True
        Game.area_map.tiles[x][y].block_sight = False


def create_v_tunnel(y1, y2, x):
    # vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        Game.area_map.tiles[x][y].is_walkable = True
        Game.area_map.tiles[x][y].block_sight = False


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


def make_map():

    # the list of objects with those two
    Game.area_map.entities = [Game.player]

    # fill map with "blocked" tiles
    Game.area_map.tiles = [
        [Tile(True) for y in range(MAP_HEIGHT)]
        for x in range(MAP_WIDTH)
    ]

    # map_type = randint(0, 2)
    # if map_type == 0:
    #    _make_dungeon()
    # elif map_type == 1:
    _make_cave()


def _make_cave():
    floor_tiles = []

    x = randint(0, MAP_WIDTH - 1)
    y = randint(0, MAP_HEIGHT - 1)

    to_make = NUM_TREES

    while to_make:
        if not Game.area_map.tiles[x][y].is_walkable:
            Game.area_map.tiles[x][y].is_walkable = True
            Game.area_map.tiles[x][y].block_sight = False
            floor_tiles.append((x, y))
            to_make -= 1

        dx = randint(-1, 1)
        dy = randint(-1, 1) if dx == 0 else 0

        x += dx
        y += dy

        if x < 0 or x >= MAP_WIDTH - 1 or y < 0 or y >= MAP_HEIGHT - 1:
            # If stuck, restart at a random floor, so everything's connected.
            restart = random.choice(floor_tiles)
            x = restart[0]
            y = restart[1]

    player_pos = random.choice(floor_tiles)
    Game.player.x = player_pos[0]
    Game.player.y = player_pos[1]
    # TODO: what if we spawned in a wall? :/
    Game.stallion.x = Game.player.x + 1
    Game.stallion.y = Game.player.y + 1
    Game.area_map.entities.append(Game.stallion)

    # Create objects/monsters by creating random "rooms"
    target = randint(MAX_ROOMS // 2, MAX_ROOMS)
    while target:
        x = randint(0, MAP_WIDTH - ROOM_MAX_SIZE)
        y = randint(0, MAP_HEIGHT - ROOM_MAX_SIZE)
        w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        room = Rect(x, y, w, h)
        place_objects(room)
        target -= 1


def _make_dungeon():

    rooms = []
    num_rooms = 0

    for r in range(MAX_ROOMS):
        # random width and height
        w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = randint(0, MAP_WIDTH - w - 1)
        y = randint(0, MAP_HEIGHT - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # this means there are no intersections, so this room is valid

            # "paint" it to the map's tiles
            create_room(new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # this is the first room, where the player starts at
                Game.player.x = new_x
                Game.player.y = new_y

            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                # draw a coin (random number that is either 0 or 1)
                if randint(0, 1):
                    # first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            # add some contents to this room, such as monsters
            place_objects(new_room)

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1


def place_objects(room):
    # choose random number of monsters
    num_monsters = randint(0, MAX_ROOM_MONSTERS)

    for i in range(num_monsters):
        # choose random spot for this monster
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        # only place it if the tile is not blocked
        if Game.area_map.is_walkable(x, y):
            choice = randint(0, 100)
            if choice <= 55:  # 55%
                name = 'bushslime'
                data = config.data.enemies.bushslime
                colour = colors.desaturated_green
            elif choice <= 85:  # 30%
                name = 'steelhawk'
                data = config.data.enemies.steelhawk
                colour = colors.light_blue
            else:  # 15%
                name = 'tigerslash'
                data = config.data.enemies.tigerslash
                colour = colors.orange
            
            monster = monster_factory.create_monster(data, x, y, colour, name)
            Game.area_map.entities.append(monster)

    # choose random number of items
    num_items = randint(0, MAX_ROOM_ITEMS)

    for i in range(num_items):
        # choose random spot for this item
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        # only place it if the tile is not blocked
        if Game.area_map.is_walkable(x, y):
            dice = randint(0, 100)
            if dice < 70:
                # create a healing potion (70% chance)
                char = '!'
                name = 'healing potion'
                color = colors.violet
                use_func = cast_heal

            elif dice < 70 + 10:
                # create a lightning bolt scroll (15% chance)
                char = '#'
                name = 'scroll of lightning bolt'
                color = colors.light_yellow
                use_func = cast_lightning

            elif dice < 70 + 10 + 10:
                # create a fireball scroll (10% chance)
                char = '#'
                name = 'scroll of fireball'
                color = colors.light_yellow
                use_func = cast_fireball

            else:
                # create a confuse scroll (15% chance)
                char = '#'
                name = 'scroll of confusion'
                color = colors.light_yellow
                use_func = cast_confuse

            item = item_factory.create_item(x, y, char, name, color, use_func)

            Game.area_map.entities.append(item)
            item.send_to_back()  # items appear below other objects


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # render the background first
    Game.panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # now render the bar on top
    if bar_width > 0:
        Game.panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # finally, some centered text with the values
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + (total_width - len(text)) // 2
    Game.panel.draw_str(x_centered, y, text, fg=colors.white, bg=None)


def get_objects_under_mouse():
    (x, y) = Game.mouse_coord

    # create a list with the names of all objects at the mouse's coordinates and in FOV
    stuff = [obj for obj in Game.area_map.entities
             if obj.x == x and obj.y == y and (obj.x, obj.y) in Game.visible_tiles]

    return stuff


def get_names_under_mouse():
    # create a list with the names of all objects at the mouse's coordinates and in FOV
    names = [obj.name for obj in get_objects_under_mouse()]

    names = ', '.join(names)  # join the names, separated by commas
    return names.capitalize()


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


def player_move_or_attack(dx, dy):

    # the coordinates the player is moving to/attacking
    x = Game.player.x + dx
    y = Game.player.y + dy

    # try to find an attackable object there
    Game.target = None
    for obj in Game.area_map.entities:
        if obj.get_component(Fighter) and obj.x == x and obj.y == y:
            Game.target = obj
            break

    # attack if target found, move otherwise
    if Game.target is not None:
        Game.player.get_component(Fighter).attack(Game.target)
    else:
        Game.player.move(dx, dy)
        Game.fov_recompute = True


def inventory_menu(header):
    # show a menu with each item of the inventory as an option
    if len(Game.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in Game.inventory]

    index = menu(header, options, INVENTORY_WIDTH)

    # if an item was chosen, return it
    if index is None or len(Game.inventory) == 0:
        return None
    return Game.inventory[index].get_component(Item)


def msgbox(text, width=50):
    menu(text, [], width)  # use menu() as a sort of "message box"


def handle_keys():
    keypress = False
    user_input = None
    while user_input is None:
        # Synchronously wait
        for event in tdl.event.get():
            if event is not None:
                user_input = event

    if event.type == 'KEYDOWN':
        user_input = event
        keypress = True
    if event.type == 'MOUSEMOTION':
        Game.mouse_coord = event.cell

    if not keypress:
        return 'didnt-take-turn'

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return 'exit'  # exit game

    if Game.game_state == 'playing':
        # movement keys
        if user_input.key == 'UP':
            player_move_or_attack(0, -1)

        elif user_input.key == 'DOWN':
            player_move_or_attack(0, 1)

        elif user_input.key == 'LEFT':
            player_move_or_attack(-1, 0)

        elif user_input.key == 'RIGHT':
            player_move_or_attack(1, 0)
        else:
            # test for other keys
            if user_input.text == 'g':
                # pick up an item
                for obj in Game.area_map.entities:  # look for an item in the player's tile
                    obj_item = obj.get_component(Item)
                    if obj.x == Game.player.x and obj.y == Game.player.y and obj_item:
                        obj_item.pick_up()
                        break

            if user_input.text == 'i':
                # show the inventory; if an item is selected, use it
                chosen_item = inventory_menu('Press the key next to an item to ' +
                                             'use it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.use()

            if user_input.text == 'd':
                # show the inventory; if an item is selected, drop it
                chosen_item = inventory_menu('Press the key next to an item to' +
                                             'drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()

            if user_input.text == 'f' and isinstance(Game.player.get_component(Fighter).weapon, Bow):
                # Unlimited arrows, or limited but we have arrows
                if not config.data.features.limitedArrows or \
                        (config.data.features.limitedArrows and Game.player.arrows > 0):
                    is_fired = False
                    is_cancelled = False
                    Game.draw_bowsight = True
                    Game.auto_target = True
                    render_all()  # show default targetting
                    while not is_fired and not is_cancelled:
                        for event in tdl.event.get():
                            if event.type == 'MOUSEMOTION':
                                Game.mouse_coord = event.cell
                                Game.auto_target = False
                                render_all()
                            elif event.type == 'KEYDOWN':
                                if event.key == 'ESCAPE':
                                    Game.draw_bowsight = False
                                    is_cancelled = True
                                elif event.char == 'f':
                                    if Game.target and Game.target.get_component(Fighter):
                                        is_critical = False
                                        damage_multiplier = config.data.weapons.arrowDamageMultiplier
                                        if config.data.features.bowCrits and randint(0,
                                                                                     100) <= config.data.weapons.bowCriticalProbability:
                                            damage_multiplier *= (1 + config.data.weapons.bowCriticalDamageMultiplier)
                                            if config.data.features.bowCritsStack:
                                                target_fighter = Game.target.get_component(Fighter)
                                                damage_multiplier += (
                                                    config.data.weapons.bowCriticalDamageMultiplier * target_fighter.bow_crits)
                                                target_fighter.bow_crits += 1
                                            is_critical = True
                                        Game.player.get_component(Fighter).attack(Game.target, damage_multiplier=damage_multiplier,
                                                              is_critical=is_critical)
                                        Game.player.arrows -= 1
                                        is_fired = True
                                        Game.draw_bowsight = False
                                        return ""

            return 'didnt-take-turn'


def target_tile(max_range=None):
    # return the position of a tile left-clicked in player's FOV (optionally in
    # a range), or (None,None) if right-clicked.
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


def target_monster(max_range=None):
    # returns a clicked monster inside FOV up to a range, or None if right-clicked
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  # player cancelled
            return None

        # return the first clicked monster, otherwise continue looping
        for obj in Game.area_map.entities:
            if obj.x == x and obj.y == y and obj.get_component(Fighter) and obj != Game.player:
                return obj


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


def cast_heal():
    # heal the player
    player_fighter = Game.player.get_component(Fighter)
    if player_fighter.hp == player_fighter.max_hp:
        message('You are already at full health.', colors.red)
        return 'cancelled'

    message('Your wounds start to feel better!', colors.light_violet)
    player_fighter.heal(HEAL_AMOUNT)


def cast_lightning():
    # find closest enemy (inside a maximum range) and damage it
    monster = closest_monster(LIGHTNING_RANGE)
    if monster is None:  # no enemy found within maximum range
        message('No enemy is close enough to strike.', colors.red)
        return 'cancelled'

    # zap it!
    message('A lighting bolt strikes the ' + monster.name + ' with a loud ' +
            'thunder! The damage is ' + str(LIGHTNING_DAMAGE) + ' hit points.',
            colors.light_blue)

    monster.get_component(Fighter).take_damage(LIGHTNING_DAMAGE)


def cast_confuse():
    # ask the player for a target to confuse
    message('Left-click an enemy to confuse it, or right-click to cancel.',
            colors.light_cyan)
    monster = target_monster(CONFUSE_RANGE)
    if monster is None:
        message('Cancelled')
        return 'cancelled'

    # replace the monster's AI with a "confused" one; after some turns it will
    # restore the old AI
    monster.set_component(ConfusedMonster(monster))
    message('The eyes of the ' + monster.name + ' look vacant, as he starts to ' +
            'stumble around!', colors.light_green)


def cast_fireball():
    # ask the player for a target tile to throw a fireball at
    message('Left-click a target tile for the fireball, or right-click to ' +
            'cancel.', colors.light_cyan)

    (x, y) = target_tile()
    if x is None:
        message('Cancelled')
        return 'cancelled'
    message('The fireball explodes, burning everything within ' +
            str(FIREBALL_RADIUS) + ' tiles!', colors.orange)

    for obj in Game.area_map.entities:  # damage every fighter in range, including the player
        obj_fighter = obj.get_component(Fighter)
        if obj.distance(x, y) <= FIREBALL_RADIUS and obj_fighter:
            message('The ' + obj.name + ' gets burned for ' +
                    str(FIREBALL_DAMAGE) + ' hit points.', colors.orange)

            obj_fighter.take_damage(FIREBALL_DAMAGE)


def save_game():
    # open a new empty shelve (possibly overwriting an old one) to write the game data
    with shelve.open('savegame', 'n') as savefile:
        savefile['tiles'] = Game.area_map.tiles
        savefile['entities'] = Game.area_map.entities
        savefile['player_index'] = Game.area_map.entities.index(Game.player)  # index of player in entities list
        savefile['inventory'] = Game.inventory
        savefile['game_msgs'] = Game.game_msgs
        savefile['game_state'] = Game.game_state


def load_game():
    # open the previously saved shelve and load the game data

    with shelve.open('savegame', 'r') as savefile:
        Game.area_map.tiles = savefile['tiles']
        Game.area_map.width = len(Game.area_map.tiles)
        Game.area_map.height = len(Game.area_map.tiles[0])
        Game.area_map.entities = savefile['entities']
        Game.player = Game.area_map.entities[savefile['player_index']]  # get index of player in objects list and access it
        Game.inventory = savefile['inventory']
        Game.game_msgs = savefile['game_msgs']
        Game.game_state = savefile['game_state']


def new_game():

    Game.player = Player()
    Game.stallion = Stallion(Game.player)

    # generate map (at this point it's not drawn to the screen)
    Game.area_map.entities = [Game.player]
    _make_cave()

    Game.game_state = 'playing'
    Game.inventory = []

    # create the list of game messages and their colors, starts empty
    Game.game_msgs = []

    # a warm welcoming message!
    message('Another brave knight yearns to bring peace to the land.', colors.red)

    # Gain four levels
    Game.player.gain_xp(40 + 80 + 160 + 320)


def play_game():

    player_action = None
    Game.mouse_coord = (0, 0)
    Game.fov_recompute = True
    Game.con.clear()  # unexplored areas start black (which is the default background color)

    while not tdl.event.is_window_closed():

        # draw all objects in the list
        render_all()

        # erase all objects at their old locations, before they move
        for obj in Game.area_map.entities:
            obj.clear()

        # handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break

        # let monsters take their turn
        if Game.game_state == 'playing' and player_action != 'didnt-take-turn':
            for obj in Game.area_map.entities:
                obj_ai = obj.get_component(AI)
                if obj_ai:
                    obj_ai.take_turn()
