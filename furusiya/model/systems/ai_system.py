from model.systems.system import System


class AISystem(metaclass=System):
    _component_name = 'ai'

    @classmethod
    def take_turn(cls, entity):
        if cls.has_ai(entity):
            ai = cls.get_ai(entity)
            ai.take_turn()
