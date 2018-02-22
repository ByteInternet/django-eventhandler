import eventhandler
import mock
from django.test import TestCase


class TestDispatcher(TestCase):

    def setUp(self):
        self.handler = mock.Mock(__name__='handler')
        eventhandler.HANDLERS = {'event_type': [self.handler]}

    def test_that_dispatcher_loads_event_defs_and_dispatches(self):
        event = {'type': 'event_type', 'payload': 'some payload'}

        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.handler.assert_called_once_with(event)

    def test_that_dispatcher_dispatches_to_multiple_handlers(self):
        other_handler = mock.Mock(__name__='other_handler')
        eventhandler.HANDLERS = {'event_type': [self.handler, other_handler]}

        event = {'type': 'event_type', 'payload': 'some payload'}
        dispatcher = eventhandler.Dispatcher()
        dispatcher.dispatch_event(event)

        self.handler.assert_called_once_with(event)
        other_handler.assert_called_once_with(event)

    def test_that_dispatcher_does_not_absorb_handler_exceptions(self):
        handler = mock.Mock(__name__='my_handler')
        handler.side_effect = RuntimeError

        eventhandler.HANDLERS = {'event_type': [handler, self.handler]}

        event = {'type': 'event_type', 'payload': 'some payload'}
        dispatcher = eventhandler.Dispatcher()

        with self.assertRaises(RuntimeError):
            dispatcher.dispatch_event(event)

    def test_that_dispatcher_absorbs_all_exceptions_when_told_to_do_so(self):
        handler = mock.Mock(__name__='my_handler')
        handler.side_effect = RuntimeError

        eventhandler.HANDLERS = {'event_type': [handler, self.handler]}

        event = {'type': 'event_type', 'payload': 'some payload'}
        dispatcher = eventhandler.Dispatcher(ignore_handler_exceptions=True)
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

    def test_that_before_handler_does_not_absorb_exceptions(self):
        before = mock.Mock(side_effect=RuntimeError)

        dispatcher = eventhandler.Dispatcher(before_handler=before)
        self.assertRaises(RuntimeError, dispatcher.dispatch_event, {'type': 'event_type'})

    def test_that_before_handler_absorbs_exceptions_when_told_to_do_so(self):
        before = mock.Mock(side_effect=RuntimeError)

        dispatcher = eventhandler.Dispatcher(before_handler=before, ignore_handler_exceptions=True)
        dispatcher.dispatch_event({'type': 'event_type'})

        before.assert_called_once_with()
        self.assertTrue(True)  # Wouldn't be reached unless Error was caught

    def test_that_dispatcher_calls_before_handler_once_for_each_event(self):
        eventhandler.HANDLERS = {'event_type': [self.handler, self.handler]}
        before = mock.Mock()

        dispatcher = eventhandler.Dispatcher(before_handler=before)
        dispatcher.dispatch_event({'type': 'event_type'})

        before.assert_called_once_with()

    def test_that_dispatcher_raises_error_if_event_has_no_type(self):
        dispatcher = eventhandler.Dispatcher()

        with self.assertRaises(RuntimeError):
            dispatcher.dispatch_event({})

    def test_that_dispatcher_does_not_raise_error_if_event_has_no_type_when_told_to(self):
        dispatcher = eventhandler.Dispatcher(error_on_missing_type=False)
        dispatcher.dispatch_event({})

        self.assertEqual(len(self.handler.mock_calls), 0)

    def test_that_handler_can_not_change_event_data_for_other_handlers(self):
        def first_handler(event):
            event['data'] = 'changed'

        eventhandler.HANDLERS = {'event_type': [first_handler, self.handler]}

        dispatcher = eventhandler.Dispatcher()

        event_tochange = {'type': 'event_type', 'data': 'not_changed'}
        dispatcher.dispatch_event(event_tochange)

        expected_handler_argument = self.handler.mock_calls[0][1][0]
        self.assertEqual(expected_handler_argument, {'type': 'event_type', 'data': 'not_changed'})

    def test_that_handler_can_not_change_event_data_for_other_handlers_if_ignore_handler_exceptions(self):
        def first_handler(event):
            event['data'] = 'changed'

        eventhandler.HANDLERS = {'event_type': [first_handler, self.handler]}

        dispatcher = eventhandler.Dispatcher(ignore_handler_exceptions=True)

        event_tochange = {'type': 'event_type', 'data': 'not_changed'}
        dispatcher.dispatch_event(event_tochange)

        expected_handler_argument = self.handler.mock_calls[0][1][0]
        self.assertEqual(expected_handler_argument, {'type': 'event_type', 'data': 'not_changed'})
