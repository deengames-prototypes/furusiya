from model.keys.events import update_callback, quit_event, mousemotion_event
from model.keys.key_callbacks import *


keybinds = {
    'ESCAPE': escape_callback,
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
    'R': continuous_rest_callback
}

events = {
    'QUIT': quit_event,
    'MOUSEMOTION': mousemotion_event
}


class KeyBinder:
    def __init__(self, game):
        self.game = game

    # Keybinds
    def register_all_keybinds(self):
        for key, callback in keybinds.items():
            self.register_keybind(key, callback)

    def suspend_all_keybinds(self):
        for key in keybinds.keys():
            self.suspend_keybind(key)

    def register_keybind(self, key, callback=None):
        callback = callback or keybinds.get(key, lambda ev: None)
        setattr(self.game.ui.app, f'key_{key}', callback)

    def suspend_keybind(self, key):
        delattr(self.game.ui.app, f'key_{key}')

    # Events
    def register_all_events(self):
        for key, callback in events.items():
            self.register_event(key, callback)

        self.register_update()

    def suspend_all_events(self):
        """You don't wanna do this. Really."""
        for key in events.keys():
            self.suspend_event(key)

    def register_event(self, event_name, callback=None):
        callback = callback or events.get(event_name, lambda ev: None)
        setattr(self.game.ui.app, f'ev_{event_name}', callback)

    def suspend_event(self, event_name):
        delattr(self.game.ui.app, f'ev_{event_name}')
        self.register_event(event_name, lambda ev: None)

    # Update
    def register_update(self, new_callback=None):
        def update(delta_time):
            self.game.renderer.render()
            new_callback(delta_time)

        callback = update if new_callback is not None else update_callback
        setattr(self.game.ui.app, 'update', callback)
