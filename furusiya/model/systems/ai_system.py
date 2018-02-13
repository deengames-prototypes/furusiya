class AISystem:
    ais = {}

    @classmethod
    def set_ai(cls, owner, ai):
        cls.ais[owner] = ai

    @classmethod
    def remove_ai(cls, owner):
        del cls.ais[owner]

    @classmethod
    def get_ai(cls, owner):
        return cls.ais.get(owner, None)

    @classmethod
    def has_ai(cls, owner):
        return cls.get_ai(owner) is not None

    @classmethod
    def take_turn(cls, entity):
        if cls.has_ai(entity):
            ai = cls.get_ai(entity)
            ai.take_turn()
