from model.maps.map_tile import MapTile

class TestMapTile:
    def test_init_turns_into_unexplored_ground(self):
        tile = MapTile()
        assert tile.is_explored == False
        assert tile.is_walkable
        assert tile.block_sight == False
        assert tile.character == '.'

    def test_convert_to_wall_makes_unwalkable_sight_blocker(self):
        # Arrange
        tile = MapTile()
        tile.is_walkable = True
        tile.block_sight = False

        # Act
        tile.convert_to_wall()

        # Assert
        assert not tile.is_walkable
        assert tile.block_sight
        assert tile.character == '#'

    def test_convert_to_ground_makes_walkable_visible_tile(self):
        # Arrange
        tile = MapTile()
        tile.is_walkable = False
        tile.block_sight = True

        # Act
        tile.convert_to_ground()

        # Assert
        assert tile.is_walkable
        assert not tile.block_sight
        assert tile.character == '.'
        