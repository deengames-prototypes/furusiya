def test_basic(obj, comp):
    assert obj.get_component(comp) is None

    c_instance = comp()
    obj.set_component(c_instance)

    assert obj.get_component(comp) is c_instance

    obj.del_component(comp)

    assert obj.get_component(comp) is None


def test_component_subclassed(obj, comp, subcomp):
    subc_instance = subcomp()
    obj.set_component(subc_instance)

    assert obj.get_component(comp) is subc_instance


def test_replace_component(obj, comp):
    obj.set_component(comp())

    new_instance = comp(10)
    obj.set_component(new_instance)

    assert obj.get_component(comp) is new_instance
    assert len(obj._components) == 1
