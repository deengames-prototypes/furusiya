from model.game_object import GameObject
from model.item import Item


def create_item(x, y, character, name, color, use_function):

    item = GameObject(x, y, character, name, color)
    item.set_component(
        Item(
            item,
            use_function=use_function
        )
    )

    return item
