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
            self.visible_tile_coordinates = self.ui_adapter.calculate_fov(
                self.player.x, self.player.y,
                # If it's walkable, it's visible!
                self.map.is_walkable, MapRenderer.FOV_ALGORITHM,
                MapRenderer.VIEW_RADIUS, MapRenderer.SHOULD_LIGHT_WALLS)

            for (x, y) in self.visible_tile_coordinates:
                self.map.tiles[x][y].is_explored = True

        # TODO: be smarter and only draw changed tiles
        # Maybe keep a list of entities and redraw tiles if they moved
        # (previously-occupied tile and new tile).
        for y in range(0, self.map.height):
            for x in range(0, self.map.width):
                tile = self.map.tiles[x][y]
                if (x, y) in self.visible_tile_coordinates:
                    self.ui_adapter.draw(x, y, tile.character, tile.colour)
                elif tile.is_explored:
                    self.ui_adapter.draw(x, y, tile.character, MapRenderer.EXPLORED_TILE_COLOUR)
                else:
                    self.ui_adapter.draw(x, y, tile.character, MapRenderer.UNEXPLORED_TILE_COLOUR)

        for e in self.map.entities:
            self.ui_adapter.draw(e.x, e.y, e.character, e.colour)

        self.ui_adapter.flush()
