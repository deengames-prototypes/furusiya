import tdl

import colors
from constants import FOV_ALGO, FOV_LIGHT_WALLS, MSG_X, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT
from main_interface import Game
from model.maps import area_map
from model.config import config
from model.systems.fighter_system import FighterSystem
from view.targeting_monster import closest_monster
from view.targeting_mouse import get_names_under_mouse


class MapRenderer:
    def __init__(self, area_map, player, ui_adapter):
        self._area_map = area_map
        self._player = player
        self._ui_adapter = ui_adapter

        self.recompute_fov = True
        self.visible_tiles = []
        self._all_tiles_rendered = False

    def render(self):
        if config.data.features.seeAllTiles and not self._all_tiles_rendered:
            for x in range(self._area_map.width):
                for y in range(self._area_map.height):
                    tile = self._area_map.tiles[x][y]
                    self._ui_adapter.con.draw_char(x, y, tile.character, tile.dark_colour)
            self._all_tiles_rendered = True

        if self.recompute_fov:
            self.recompute_fov = False
            # The current FOV is changing. Draw everything in it with the "explored"
            # style (because it was in the FOV, so it is explored).
            for (x, y) in self.visible_tiles:
                tile = self._area_map.tiles[x][y]
                self._ui_adapter.con.draw_char(x, y, tile.character, tile.dark_colour)

            # Due to lightWalls being set to true, we need to filter "walls" that are out of bounds.
            self.visible_tiles = area_map.filter_tiles(
                self._ui_adapter.calculate_fov(
                    self._player.x, self._player.y,
                    self._area_map.is_visible_tile,
                    FOV_ALGO,
                    config.data.player.lightRadius,
                    FOV_LIGHT_WALLS
                ),
                self._area_map.is_on_map
            )

            for (x, y) in self.visible_tiles:
                self._area_map.tiles[x][y].is_explored = True

        # Draw everything in the current FOV
        for (x, y) in self.visible_tiles:
            tile = self._area_map.tiles[x][y]
            self._ui_adapter.con.draw_char(x, y, tile.character, tile.colour)

        for e in self._area_map.entities:
            if e is self._player:
                continue
            e.draw()

        if Game.draw_bowsight:
            Game.target = closest_monster(config.data.player.lightRadius) if Game.auto_target else None
            x2, y2 = (Game.target.x, Game.target.y) if Game.target is not None else Game.mouse_coord

            x1, y1 = self._player.x, self._player.y
            line = tdl.map.bresenham(x1, y1, x2, y2)
            monster_on_target_tile = [x for x in self._area_map.get_entities_on(x2, y2) if FighterSystem.has_fighter(x)]
            for pos in line:
                if pos in self.visible_tiles:
                    if pos == (x2, y2) and monster_on_target_tile:
                        self._ui_adapter.con.draw_char(pos[0], pos[1], 'X', fg=colors.red)
                    else:
                        self._ui_adapter.con.draw_char(pos[0], pos[1], '*', colors.dark_green, bg=None)

        self._player.draw()

        # blit the contents of "self._ui_adapter.con" to the root console and present it
        self._ui_adapter.root.blit(self._ui_adapter.con, 0, 0, self._area_map.width, self._area_map.height, 0, 0)

        # prepare to render the GUI self._ui_adapter.panel
        self._ui_adapter.panel.clear(fg=colors.white, bg=colors.black)

        # print the game messages, one line at a time
        y = 1
        for (line, color) in Game.game_msgs:
            self._ui_adapter.panel.draw_str(MSG_X, y, line, bg=None, fg=color)
            y += 1

        # show the player's stats
        player_fighter = FighterSystem.get_fighter(self._player)
        self._ui_adapter.panel.draw_str(1, 1, "HP: {}/{}".format(player_fighter.hp, player_fighter.max_hp))

        # display names of objects under the mouse
        self._ui_adapter.panel.draw_str(1, 0, get_names_under_mouse(), bg=None, fg=colors.light_gray)

        # blit the contents of "self._ui_adapter.panel" to the root console
        self._ui_adapter.root.blit(self._ui_adapter.panel, 0, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0)

        self._ui_adapter.flush()

    def clear(self):
        self._ui_adapter.clear()

    def refresh_all(self):
        for x in range(self._area_map.width):
            for y in range(self._area_map.height):
                tile = self._area_map.tiles[x][y]
                if tile.is_explored:
                    self._ui_adapter.con.draw_char(x, y, tile.character, tile.dark_colour)
