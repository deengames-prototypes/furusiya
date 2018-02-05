from legacy.io.config_watcher import ConfigWatcher


class MapRenderer:
    
    # For explored/unexplored tiles
    EXPLORED_TILE_COLOUR = (64, 64, 64)

    # FOV constants
    FOV_ALGORITHM = 'BASIC'  # default FOV algorithm
    SHOULD_LIGHT_WALLS = True
    VIEW_RADIUS = 5

    def __init__(self, area_map, player, ui_adapter):
        self.recompute_fov = True
        self._area_map = area_map
        self._player = player
        self._ui_adapter = ui_adapter
        self._visible_tile_coordinates = []

    def render(self):
        if ConfigWatcher.instance.has("seeAll"):
            for x in range(self._area_map.width):
                for y in range(self._area_map.height):
                    self._ui_adapter.draw(x, y, self._area_map.tiles[x][y].character, (128, 128, 128))

        if self.recompute_fov:
            self.recompute_fov = False            
            # The current FOV is changing. Draw everything in it with the "explored"
            # style (because it was in the FOV, so it is explored).
            for (x, y) in self._visible_tile_coordinates:
                tile = self._area_map.tiles[x][y]
                self._ui_adapter.draw(x, y, tile.character, MapRenderer.EXPLORED_TILE_COLOUR)

            self._visible_tile_coordinates = self._ui_adapter.calculate_fov(
                self._player.x, self._player.y,
                # If it's walkable, it's visible!
                self._area_map.is_walkable, MapRenderer.FOV_ALGORITHM,
                MapRenderer.VIEW_RADIUS, MapRenderer.SHOULD_LIGHT_WALLS)

            # Prune out things that are in our FOV but are out of bounds
            self._visible_tile_coordinates = [
                (x, y)
                for (x, y) in self._visible_tile_coordinates
                if self._area_map.is_on_map(x, y)
            ]

            for (x, y) in self._visible_tile_coordinates:
                self._area_map.tiles[x][y].is_explored = True
        
        # Draw everything in the current FOV
        for (x, y) in self._visible_tile_coordinates:
            tile = self._area_map.tiles[x][y]
            self._ui_adapter.draw(x, y, tile.character, tile.colour)

        for e in self._area_map.entities:
            if (e.x, e.y) in self._visible_tile_coordinates:
                self._ui_adapter.draw(e.x, e.y, e.character, e.colour)

        self._ui_adapter.flush()
