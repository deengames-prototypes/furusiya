class MapRenderer:
    
    # For explored/unexplored tiles
    UNEXPLORED_TILE_COLOUR = (0, 0, 0)
    EXPLORED_TILE_COLOUR = (64, 64, 64)

    # FOV constants
    FOV_ALGORITHM = 'BASIC'  #default FOV algorithm
    SHOULD_LIGHT_WALLS = True
    VIEW_RADIUS = 5

    def __init__(self, map, player, ui_adapter):
        self.map = map
        self.player = player
        self.ui_adapter = ui_adapter
        self.recompute_fov = True
        self.visible_tile_coordinates = []

    def render(self):
        if self.recompute_fov:
            self.recompute_fov = False            
            # The current FOV is changing. Draw everything in it with the "explored"
            # style (because it was in the FOV, so it is explored).
            for (x, y) in self.visible_tile_coordinates:
                tile = self.map.tiles[x][y]
                self.ui_adapter.draw(x, y, tile.character, MapRenderer.EXPLORED_TILE_COLOUR)

            self.visible_tile_coordinates = self.ui_adapter.calculate_fov(
                self.player.x, self.player.y,
                # If it's walkable, it's visible!
                self.map.is_walkable, MapRenderer.FOV_ALGORITHM,
                MapRenderer.VIEW_RADIUS, MapRenderer.SHOULD_LIGHT_WALLS)

            # Prune out things that are in our FOV but are out of bounds
            self.visible_tile_coordinates = [(x, y) for (x, y) in self.visible_tile_coordinates if self.map.is_on_map(x, y)]

            for (x, y) in self.visible_tile_coordinates:
                self.map.tiles[x][y].is_explored = True
        
        # Draw everything in the current FOV
        for (x, y) in self.visible_tile_coordinates:
            tile = self.map.tiles[x][y]
            self.ui_adapter.draw(x, y, tile.character, tile.colour)

        for e in self.map.entities:
            if (e.x, e.y) in self.visible_tile_coordinates:
                self.ui_adapter.draw(e.x, e.y, e.character, e.colour)

        self.ui_adapter.flush()
