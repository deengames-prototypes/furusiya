class Component:
    """
    Basic class describing a component.

    Attributes:
        owner (GameObject): The object who this component belongs to
    """
    def __init__(self, owner):
        self.owner = owner
