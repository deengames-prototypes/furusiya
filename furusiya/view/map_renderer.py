import colors
from constants import FOV_ALGO, FOV_LIGHT_WALLS, MSG_X
from game import Game
from model.maps import area_map
from model.config import config
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
                    self._ui_adapter.con.draw_str(x, y, tile.character, tile.dark_colour)
            self._all_tiles_rendered = True

        if self.recompute_fov:
            self.recompute_fov = False
            # The current FOV is changing. Draw everything in it with the "explored"
            # style (because it was in the FOV, so it is explored).
            for (x, y) in self.visible_tiles:
                tile = self._area_map.tiles[x][y]
                self._ui_adapter.con.draw_str(x, y, tile.character, tile.dark_colour)

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
            self._ui_adapter.con.draw_str(x, y, tile.character, tile.colour)

        for e in self._area_map.entities:
            if e is self._player:
                continue
            e.draw()

        if Game.draw_bowsight:
            Game.target = closest_monster(config.data.player.lightRadius) if Game.auto_target else None
            x2, y2 = (Game.target.x, Game.target.y) if Game.target is not None else Game.mouse_coord

            x1, y1 = self._player.x, self._player.y
            line = Game.ui.bresenham(x1, y1, x2, y2)
            monster_on_target_tile = [x for x in self._area_map.get_entities_on(x2, y2) if Game.fighter_system.has(x)]
            for pos in line:
                if pos in self.visible_tiles:
                    if pos == (x2, y2) and monster_on_target_tile:
                        self._ui_adapter.con.draw_str(pos[0], pos[1], 'X', fg=colors.red)
                    else:
                        self._ui_adapter.con.draw_str(pos[0], pos[1], '*', colors.dark_green)

        self._player.draw()

        # prepare to render the GUI self._ui_adapter.panel
        self._ui_adapter.panel.clear(fg=colors.white, bg=colors.black)

        # print the game messages, one line at a time
        y = 1
        for (line, color) in Game.game_messages:
            self._ui_adapter.panel.draw_str(MSG_X, y, line, fg=color)
            y += 1

        # show the player's stats
        self._ui_adapter.panel.draw_str(1, 1, "PLAYER")

        player_fighter = Game.fighter_system.get(self._player)
        skill_component = Game.skill_system.get(self._player)
        xp_component = Game.xp_system.get(self._player)

        self._ui_adapter.panel.draw_str(11, 1, "LEVEL {}".format(xp_component.level))
        self._ui_adapter.panel.draw_str(10, 2, "HP: {}/{}".format(player_fighter.hp, player_fighter.max_hp))
        self._ui_adapter.panel.draw_str(10, 3, "SP: {}/{}".format(skill_component.skill_points,
                                                                  config.data.player.maxSkillPoints))

        # show the horse's stats, if mounted
        if config.data.stallion.enabled:
            self._ui_adapter.panel.draw_str(1, 4, "STALLION")

            stallion_fighter = Game.fighter_system.get(Game.stallion)
            skill_component = Game.skill_system.get(Game.stallion)

            self._ui_adapter.panel.draw_str(10, 5, "HP: {}/{}".format(stallion_fighter.hp, stallion_fighter.max_hp))
            self._ui_adapter.panel.draw_str(10, 6, "SP: {}/{}".format(skill_component.skill_points,
                                                                      config.data.stallion.maxSkillPoints))

        # display names of objects under the mouse
        self._ui_adapter.panel.draw_str(1, 0, get_names_under_mouse(), fg=colors.light_gray)

        self._ui_adapter.flush()

    def refresh_all(self):
        for x in range(self._area_map.width):
            for y in range(self._area_map.height):
                tile = self._area_map.tiles[x][y]
                if tile.is_explored:
                    self._ui_adapter.con.draw_str(x, y, tile.character, tile.dark_colour)
                else:
                    self._ui_adapter.con.draw_str(x, y, ' ')
