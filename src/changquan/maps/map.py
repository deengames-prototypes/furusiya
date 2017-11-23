class Map:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []

        # Create a 2D structure of tiles
        for x in range(0, self.width):
            self.tiles.append([])
            for y in range(0, self.height):
                self.tiles[x].append(MapTile())
                

class MapTile:
    def __init__(self):
        self.is_walkable = True
        self.character = '.'
        self.colour = (128, 128, 128)