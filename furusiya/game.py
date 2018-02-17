class GameMetaClass(type):
    def __new__(mcs, class_name, bases, dct):

        dct['_player'] = 0
        dct['_stallion'] = 0
        dct['area_map'] = None

        return type.__new__(mcs, class_name, bases, dct)

    @property
    def player(cls):
        return cls.area_map.get_entity_with_id(cls._player)

    @player.setter
    def player(cls, value):
        cls._player = value

    @property
    def stallion(cls):
        return cls.area_map.get_entity_with_id(cls._stallion)
    
    @stallion.setter
    def stallion(cls, value):
        cls._stallion = value


class Game(metaclass=GameMetaClass):
    inventory = []
    draw_bowsight = None
    mouse_coord = (0, 0)
    auto_target = None
    target = None
    game_messages = []
    game_state = None

    area_map = None
    renderer = None
    ui = None
    current_turn = None

    save_manager = None
    keybinder = None

    fighter_sys = None
    ai_sys = None
    xp_sys = None

    # indexes refering to actual objects in area_map.entities
    # refer to above metaclass for actual properties
    _player = 0
    _stallion = 0

    # list of attribute names to not pickle
    _dont_pickle = ['_dont_pickle', 'ui', 'renderer', 'save_manager']
