import math

from main_interface import Game, get_blocking_object_at


class GameObject:
    """
    this is a generic object: the player, a monster, an item, the stairs...
    it's always represented by a character on screen.
    """
    def __init__(self, x, y, char, name, color, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

        self._components = {}

    def _get_components_of_type(self, component_type):
        return [
            k
            for k in self._components.keys()
            if k == component_type
        ]

    def _get_component_type(self, component_type):
        possible_matches = self._get_components_of_type(component_type)

        if len(possible_matches) == 0:
            return None
        else:
            return possible_matches[0]

    def set_component(self, component):
        self._components[type(component)] = component

    def get_component(self, component_type):
        return self._components.get(self._get_component_type(component_type), None)

    def remove_component(self, component_type):
        try:
            del self._components[self._get_component_type(component_type)]
        except KeyError:
            pass

    def has_component(self, component_type):
        return self.get_component(component_type) is not None

    def move(self, dx, dy):
        # move by the given amount, if the destination is not blocked
        if Game.area_map.is_walkable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
        else:
            return get_blocking_object_at(self.x + dx, self.y + dy)

    def move_towards(self, target_x, target_y):
        # vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # normalize it to length 1 (preserving direction), then round it and
        # convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return self.move(dx, dy)

    def distance_to(self, other):
        # return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        # return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def send_to_back(self):
        # make this object be drawn first, so all others appear above it if
        # they're in the same tile.
        Game.area_map.entities.remove(self)
        Game.area_map.entities.insert(0, self)

    def draw(self):
        # only show if it's visible to the player
        if (self.x, self.y) in Game.renderer.visible_tiles:
            # draw the character that represents this object at its position
            Game.ui.con.draw_char(self.x, self.y, self.char, self.color, bg=None)

    def clear(self):
        # erase the character that represents this object
        Game.ui.con.draw_char(self.x, self.y, ' ', self.color, bg=None)
