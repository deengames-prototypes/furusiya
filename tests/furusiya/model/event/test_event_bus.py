from unittest.mock import Mock

from model.event.event_bus import EventBus


class TestEventBus:
    def test_bind_registers_event(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callbacks = [Mock(), Mock(), Mock()]

        for callback in callbacks:
            event_bus.bind(event_name, callback)

        assert event_bus.events[event_name] == callbacks

    def test_unbind_unregisters_event(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callback = Mock()
        event_bus.bind(event_name, callback)

        event_bus.unbind(event_name, callback)

        assert event_bus.events[event_name] == []

    def test_trigger_triggers_event(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callback = Mock()
        event_bus.bind(event_name, callback)

        event_bus.trigger(event_name)

        assert callback.called

    def test_trigger_triggers_event_with_arguments(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callback = Mock()
        args = [1, 'test', ';']
        kwargs = {'size': (4, 5)}
        event_bus.bind(event_name, callback)

        event_bus.trigger(event_name, *args, **kwargs)

        callback.assert_called_with(*args, **kwargs)
