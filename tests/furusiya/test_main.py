from game import Game
from main import new_game
from model.config import config


def test_new_game_creates_new_game():
    """Too slow to split into multiple tests."""
    new_game()

    assert Game.instance.area_map is not None
    assert (Game.instance.area_map.width, Game.instance.area_map.height) != (0, 0)
    assert Game.instance.area_map.tiles != []  # map has been generated

    assert Game.instance.player is not None

    if config.data.stallion.enabled:
        assert Game.instance.stallion is not None

        assert (Game.instance.stallion.x, Game.instance.stallion.y) in (
            (dx + Game.instance.player.x, dy + Game.instance.player.y)
            for dx in range(-5, 6)  # make sure stallion is within 5 tiles from the player
            for dy in range(-5, 6)  # in fact, it could be farther, but that's highly unlikely.
        )

    assert Game.instance.xp_system.get(Game.instance.player).level == 5

    assert Game.instance.inventory is not None
    assert Game.instance.inventory == []

    assert Game.instance.game_state is not None
    assert Game.instance.game_state == 'playing'

    assert Game.instance.game_messages is not None
    assert len(Game.instance.game_messages) == 5  # 1 welcoming message, 4 level up messages.

    old_tile = (Game.instance.player.x, Game.instance.player.y)
    assert Game.instance.area_map.tiles[Game.instance.player.x][Game.instance.player.y].is_walkable

    new_game()
    new_tile = (Game.instance.player.x, Game.instance.player.y)
    assert Game.instance.area_map.tiles[Game.instance.player.x][Game.instance.player.y].is_walkable

    assert old_tile != new_tile
