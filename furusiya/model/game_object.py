import math

from main_interface import Game, is_blocked, get_blocking_object_at


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

        self.ai = None

        self._components = {}

    def _get_type(self, type_):
        possible_matches = [
            k
            for k in self._components.keys()
            if issubclass(k, type_)
        ]

        if len(possible_matches) == 0:
            return None
        else:
            return possible_matches[0]

    def set_component(self, component):
        self._components[type(component)] = component

    def get_component(self, type_):
        return self._components.get(self._get_type(type_), None)

    def del_component(self, type_):
        try:
            del self._components[self._get_type(type_)]
        except KeyError:
            pass

    def move(self, dx, dy):
        # move by the given amount, if the destination is not blocked
        if not is_blocked(self.x + dx, self.y + dy):
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
        Game.objects.remove(self)
        Game.objects.insert(0, self)

    def draw(self):
        # only show if it's visible to the player
        if (self.x, self.y) in Game.visible_tiles:
            # draw the character that represents this object at its position
            Game.con.draw_char(self.x, self.y, self.char, self.color, bg=None)

    def clear(self):
        # erase the character that represents this object
        Game.con.draw_char(self.x, self.y, ' ', self.color, bg=None)
