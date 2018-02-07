class Component:
    """
    Basic class describing a component.

    Since all components inherit from this, it shouldn't be passed to GameObject's get_component method;
    lest it returns a random component.

    Attributes:
        owner (GameObject): The object who this component belongs to
    """
    def __init__(self, owner):
        self.owner = owner
