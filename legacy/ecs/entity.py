class Entity:
    def __init__(self, character, colour):
        self._components = {}
        self.x = 0
        self.y = 0
        self.character = character
        self.colour = colour

    def set(self, component):
        key = type(component)
        self._components[key] = component
        
    def get(self, component_type):
        return self._components[component_type]