class EventBus:
    def __init__(self):
        self.events = {}

    def _create_data_structure(self, event_name):
        if not isinstance(self.events.get(event_name, None), list):
            self.events[event_name] = []

    def trigger(self, event_name, *args, **kwargs):
        if self.events.get(event_name, None):
            for callback in self.events[event_name]:
                callback(*args, **kwargs)

    def bind(self, event_name, event_callback):
        self._create_data_structure(event_name)
        self.events[event_name].append(event_callback)

    def unbind(self, event_name, event_callback):
        if self.events.get(event_name, None):
            self.events[event_name].remove(event_callback)
