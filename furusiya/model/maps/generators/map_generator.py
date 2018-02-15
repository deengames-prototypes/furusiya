import random

from model import item_callbacks
from model.config import config
from model.factories import item_factory
from model.factories import monster_factory
import colors

def generate_monsters(area_map, num_monsters):
    for i in range(num_monsters):
        # choose random spot for this monster
        x = random.randint(0, area_map.width)
        y = random.randint(0, area_map.width)

        # only place it if the tile is not blocked
        if area_map.is_walkable(x, y):
            choice = random.randint(0, 100)
            if choice <= 55: 
                name = 'bushslime'
                data = config.data.enemies.bushslime
                colour = colors.desaturated_green
            elif choice <= 55 + 30:
                name = 'steelhawk'
                data = config.data.enemies.steelhawk
                colour = colors.light_blue
            else:  # 15
                name = 'tigerslash'
                data = config.data.enemies.tigerslash
                colour = colors.orange

            monster = monster_factory.create_monster(data, x, y, colour, name)
            area_map.entities.append(monster)

def generate_items(area_map, num_items):
    for i in range(num_items):
        # choose random spot for this item
        x = random.randint(0, area_map.width)
        y = random.randint(0, area_map.width)

        # only place it if the tile is not blocked
        if area_map.is_walkable(x, y):
            dice = random.randint(0, 100)
            if dice < 70:
                # create a healing potion (70% chance)
                char = '!'
                name = 'healing potion'
                color = colors.violet
                use_func = item_callbacks.cast_heal

            elif dice < 70 + 10:
                # create a lightning bolt scroll (15% chance)
                char = '#'
                name = 'scroll of lightning bolt'
                color = colors.light_yellow
                use_func = item_callbacks.cast_lightning

            elif dice < 70 + 10 + 10:
                # create a fireball scroll (10% chance)
                char = '#'
                name = 'scroll of fireball'
                color = colors.light_yellow
                use_func = item_callbacks.cast_fireball

            else: # 10
                # create a confuse scroll (15% chance)
                char = '#'
                name = 'scroll of confusion'
                color = colors.light_yellow
                use_func = item_callbacks.cast_confuse

            item = item_factory.create_item(x, y, char, name, color, use_func)

            area_map.entities.append(item)
            item.send_to_back()  # items appear below other objects
