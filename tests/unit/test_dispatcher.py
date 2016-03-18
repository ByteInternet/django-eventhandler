import eventhandler
import mock
from django.test import TestCase


class TestDispatcher(TestCase):

    def setUp(self):
        self.handler = mock.Mock()
        eventhandler.HANDLERS = {'event_type': [self.handler]}

    def test_that_dispatcher_loads_event_defs_and_dispatches(self):
        event = {'type': 'event_type', 'payload': 'some payload'}

        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.handler.assert_called_once_with(event)

    def test_that_dispatcher_dispatches_to_multiple_handlers(self):
        other_handler = mock.Mock()
        eventhandler.HANDLERS = {'event_type': [self.handler, other_handler]}

        event = {'type': 'event_type', 'payload': 'some payload'}
        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.handler.assert_called_once_with(event)
        other_handler.assert_called_once_with(event)

    def test_that_dispatcher_absorbs_all_exceptions(self):
        handler = mock.Mock()
        handler.side_effect = RuntimeError

        eventhandler.HANDLERS = {'event_type': [handler, self.handler]}

        event = {'type': 'event_type', 'payload': 'some payload'}
        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.handler.assert_called_once_with(event)

    def test_that_dispatcher_absorbs_events_without_handler(self):
        event = {'type': 'unknown_type', 'payload': 'some payload'}
        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.assertEqual(len(self.handler.mock_calls), 0)

    def test_that_dispatcher_calls_before_handler(self):
        before = mock.Mock()

        dispatcher = eventhandler.Dispatcher(before_handler=before)
        dispatcher.dispatch_event({'type': 'event_type'})

        before.assert_called_once_with()

    def test_that_dispatcher_calls_before_handler_once_for_each_event(self):
        eventhandler.HANDLERS = {'event_type': [self.handler, self.handler]}
        before = mock.Mock()

        dispatcher = eventhandler.Dispatcher(before_handler=before)
        dispatcher.dispatch_event({'type': 'event_type'})

        before.assert_called_once_with()
