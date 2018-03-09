class GameMetaClass(type):
    def __new__(mcs, class_name, bases, dct):
        cls = type.__new__(mcs, class_name, bases, dct)
        cls._instance = cls()
        return cls

    def __getattr__(cls, item):
        return cls._instance.__dict__.get(item)

    def __setattr__(cls, key, value):
        if key == '_instance':
            super().__setattr__(key, value)
        cls._instance.__setattr__(key, value)


class Game(metaclass=GameMetaClass):
    _instance = None
    _dont_pickle = {'ui', 'save_manager', 'keybinder', 'renderer'}

    def __init__(self):
        self.inventory = []
        self.draw_bowsight = None
        self.mouse_coord = (0, 0)
        self.auto_target = None
        self.target = None
        self.game_messages = []
        self.game_state = None

        self.area_map = None
        self.renderer = None
        self.ui = None
        self.current_turn = None

        self.save_manager = None
        self.keybinder = None

        self.fighter_system = None
        self.ai_system = None
        self.xp_system = None
        self.skill_system = None

        self.player = None
        self.stallion = None

        self.random = None
        self.floors = []
        self.current_floor = 1
