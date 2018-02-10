class AISystem:
    ais = {}

    @classmethod
    def take_monster_turns(cls):
        for ai in cls.ais.values():
            ai.take_turn()

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
