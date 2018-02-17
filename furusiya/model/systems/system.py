class ComponentSystem:
    """
    Base class for component systems.
    """
    def __init__(self):
        self.component_dict = {}

    def set(self, owner, component):
        self.component_dict[owner.id] = component

    def remove(self, owner):
        del self.component_dict[owner.id]

    def get(self, owner):
        return self.component_dict.get(owner.id, None)

    def has(self, owner):
        return self.get(owner) is not None
