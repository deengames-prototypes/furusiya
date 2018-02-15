class System(type):
    """
    Metaclass for component systems.

    Automatically generates set_, remove_, get_, and has_
    methods according to the class's _component_name attribute.

    Also creates a dictionary of owner entities and objects
    using the same name, appending the letter 's'.
    """
    def __new__(mcs, clsname, bases, dct):
        component_name = dct['_component_name']

        # This sets the local variable `component_dict`
        # and the class attribute in question to the same dictionary instance
        # for easier method generation
        dct[f'{component_name}s'] = component_dict = {}

        def set_(owner, component):
            component_dict[owner] = component

        def remove_(owner):
            del component_dict[owner]

        def get_(owner):
            return component_dict.get(owner, None)

        def has_(owner):
            return get_(owner) is not None

        # They don't need to be classmethods;
        # we can access the component dictionary locally. See above.
        dct[f'set_{component_name}'] = staticmethod(set_)
        dct[f'remove_{component_name}'] = staticmethod(remove_)
        dct[f'get_{component_name}'] = staticmethod(get_)
        dct[f'has_{component_name}'] = staticmethod(has_)

        return type.__new__(mcs, clsname, bases, dct)
