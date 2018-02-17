from model.keys.callbacks import update_callback, quit_event, mousemotion_event
from model.keys.key_callbacks import *


keybinds = {
    'ESCAPE': exit_to_main_menu_callback,
    'ENTER': enter_callback,

    'UP': up_callback,
    'DOWN': down_callback,
    'LEFT': left_callback,
    'RIGHT': right_callback,

    'g': pickup_callback,

    'i': inventory_use,
    'd': inventory_drop,

    'f': bow_callback,
    'm': mount_callback,

    'r': rest_callback,
    'R': continuous_rest_callback,

    'l': whirlwind_callback
}

events = {
    'QUIT': quit_event,

    'MOUSEMOTION': mousemotion_event,
    'MOUSEDOWN': None,
    'MOUSEUP': None,

    'KEYDOWN': None,
    'KEYUP': None,
}


class KeyBinder:
    def __init__(self, game):
        self.game = game

    @staticmethod
    def _format_attr_key(key_name):
        return f'key_{key_name}'

    @staticmethod
    def _format_attr_event(event_name):
        return f'ev_{event_name}'

    # Keybinds
    def register_all_keybinds(self):
        for key, callback in keybinds.items():
            self.register_keybind(key, callback)

    def suspend_all_keybinds(self):
        for key in keybinds.keys():
            self.suspend_keybind(key)

    def register_keybind(self, key, callback=None):
        callback = callback or keybinds.get(key) or (lambda ev: None)
        setattr(self.game.ui.app, self._format_attr_key(key), callback)

    def suspend_keybind(self, key):
        delattr(self.game.ui.app, self._format_attr_key(key))

    # Events
    def register_all_events(self):
        for key, callback in events.items():
            self.register_event(key, callback)

        self.register_update()

    def register_event(self, event_name, callback=None):
        callback = callback or events.get(event_name) or (lambda ev: None)
        setattr(self.game.ui.app, self._format_attr_event(event_name), callback)

    # Update
    def register_update(self, new_callback=None):
        def update(delta_time):
            self.game.renderer.render()
            new_callback(delta_time)

        callback = update if new_callback is not None else update_callback
        setattr(self.game.ui.app, 'update', callback)
