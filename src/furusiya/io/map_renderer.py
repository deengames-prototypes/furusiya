class MapRenderer:
    def __init__(self, map, ui_adapter):
        self.map = map
        self.ui_adapter = ui_adapter

    def render(self):
        # TODO: be smarter and only draw changed tiles
        # Maybe keep a list of entities and redraw tiles if they moved
        # (previously-occupied tile and new tile).
        for y in range(0, self.map.height):
            for x in range(0, self.map.width):
                tile = self.map.tiles[x][y]
                self.ui_adapter.draw(x, y, tile.character, tile.colour)

        for e in self.map.entities:
            self.ui_adapter.draw(e.x, e.y, e.character, e.colour)

        self.ui_adapter.flush()
