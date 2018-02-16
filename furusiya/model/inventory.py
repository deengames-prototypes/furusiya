from constants import INVENTORY_WIDTH
from main_interface import Game
from model.item import Item


def inventory_menu(header):
    # show a menu with each item of the inventory as an option
    if len(Game.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in Game.inventory]

    index = Game.ui.create_menu(header, options, INVENTORY_WIDTH)

    # if an item was chosen, return it
    if index is None or len(Game.inventory) == 0:
        return None
    return Game.inventory[index].get_component(Item)
