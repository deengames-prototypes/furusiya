class System(type):
    def __new__(mcs, clsname, bases, dct):
        component_name = dct['_component_name']

        def set_(cls, owner, component):
            getattr(cls, f'{component_name}s')[owner] = component

        def remove_(cls, owner):
            del getattr(cls, f'{component_name}s')[owner]

        def get_(cls, owner):
            return getattr(cls, f'{component_name}s').get(owner, None)

        def has_(cls, owner):
            return getattr(cls, f'get_{component_name}')(owner) is not None

        dct[f'set_{component_name}'] = classmethod(set_)
        dct[f'remove_{component_name}'] = classmethod(remove_)
        dct[f'get_{component_name}'] = classmethod(get_)
        dct[f'has_{component_name}'] = classmethod(has_)
        dct[f'{component_name}s'] = {}

        return type.__new__(mcs, clsname, bases, dct)
