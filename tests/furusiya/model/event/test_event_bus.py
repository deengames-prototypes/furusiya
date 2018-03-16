from unittest.mock import Mock

from model.event.event_bus import EventBus


class TestEventBus:
    def test_bind_registers_event(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callbacks = [Mock(), Mock(), Mock()]

        for callback in callbacks:
            event_bus.bind(event_name, callback)

        assert event_bus.events[event_bus.default_owner][event_name] == callbacks

    def test_bind_registers_event_with_owner(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callbacks = [Mock(), Mock(), Mock()]
        owner = Mock()

        for callback in callbacks:
            event_bus.bind(event_name, callback, owner)

        assert event_bus.events[owner][event_name] == callbacks

    def test_unbind_unregisters_event(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callback = Mock()

        event_bus.bind(event_name, callback)
        assert event_bus.events[event_bus.default_owner][event_name] == [callback]

        event_bus.unbind(event_name, callback)
        assert event_bus.events[event_bus.default_owner][event_name] == []

    def test_unbind_unregisters_event_with_owner(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callback = Mock()
        owner = Mock()

        event_bus.bind(event_name, callback, owner)
        assert event_bus.events[owner][event_name] == [callback]

        event_bus.unbind(event_name, callback, owner)
        assert event_bus.events[owner][event_name] == []

    def test_trigger_triggers_event(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callback = Mock()
        event_bus.bind(event_name, callback)

        event_bus.trigger(event_name)

        assert callback.called

    def test_trigger_triggers_events_from_multiple_owners(self):
        event_bus = EventBus()
        event_name = 'event 1'
        callbacks = [Mock(), Mock(), Mock()]

        event_bus.bind(event_name, callbacks[0])
        event_bus.bind(event_name, callbacks[1], Mock())
        event_bus.bind(event_name, callbacks[2], Mock())

        event_bus.trigger(event_name)

        for callback in callbacks:
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

    def test_unregister_removes_owners_events(self):
        event_bus = EventBus()
        event1 = 'event 1'
        event2 = 'event 2'
        callbacks = [Mock(), Mock()]
        owner = Mock()
        free_callbacks = [Mock(), Mock()]

        event_bus.bind(event1, callbacks[0], owner)
        event_bus.bind(event2, callbacks[1], owner)

        event_bus.bind(event1, free_callbacks[0])
        event_bus.bind(event2, free_callbacks[1])

        event_bus.unregister(owner)

        assert event_bus.events.get(owner, None) is None
        assert event_bus.events.get(event_bus.default_owner, None) is not None
