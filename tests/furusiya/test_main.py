from game import Game
from main import new_game
from model.systems.xp_system import XPSystem


def test_new_game_creates_new_game():
    """Too slow to split into multiple tests."""
    new_game()

    assert Game.area_map is not None
    assert (Game.area_map.width, Game.area_map.height) != (0, 0)
    assert Game.area_map.tiles != []  # map has been generated

    assert Game.player is not None
    assert Game.stallion is not None

    assert (Game.stallion.x, Game.stallion.y) in (
        (x + Game.player.x, y + Game.player.y)
        for x, y in (
            (dx, dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
        )
    )

    assert XPSystem.get_experience(Game.player).level == 5

    assert Game.inventory is not None
    assert Game.inventory == []

    assert Game.game_state is not None
    assert Game.game_state == 'playing'

    assert Game.game_msgs is not None
    assert len(Game.game_msgs) == 5  # 1 welcoming message, 4 level up messages.

    old_tile = (Game.player.x, Game.player.y)
    assert Game.area_map.tiles[Game.player.x][Game.player.y].is_walkable

    new_game()
    new_tile = (Game.player.x, Game.player.y)
    assert Game.area_map.tiles[Game.player.x][Game.player.y].is_walkable

    assert old_tile != new_tile
