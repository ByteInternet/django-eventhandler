import eventhandler
import mock
from django.test import TestCase


class TestDispatcher(TestCase):

    def setUp(self):
        mock_close = mock.patch('eventhandler.close_old_connections')
        self.close_old_connections = mock_close.start()
        self.addCleanup(mock_close.stop)

        self.handler = mock.Mock()
        eventhandler.HANDLERS = {'event_type': [self.handler]}

    def test_that_dispatcher_loads_event_defs_and_dispatches(self):
        event = {'type': 'event_type', 'payload': 'some payload'}

        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.handler.assert_called_once_with(event)

    def test_that_dispatcher_closes_old_connections(self):
        event = {'type': 'event_type', 'payload': 'some payload'}
        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.close_old_connections.assert_called_once_with()

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

    def test_that_dispatcher_absorbs_invalid_events(self):
        event = {'payload': 'not a valid event'}
        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.assertEqual(len(self.handler.mock_calls), 0)
