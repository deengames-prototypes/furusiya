class EventBus:
    def __init__(self):
        self.events = {}

    def _ensure_exists(self, event_name):
        if not isinstance(self.events.get(event_name, None), list):
            self.events[event_name] = []

    def tigger(self, event_name, *args, **kwargs):
        self._ensure_exists(event_name)

        for callback in self.events[event_name]:
            callback(*args, **kwargs)

    def bind(self, event_name, event_callback):
        self._ensure_exists(event_name)
        self.events[event_name].append(event_callback)

    def unbind(self, event_name, event_callback):
        self._ensure_exists(event_name)
        self.events[event_name].remove(event_callback)
