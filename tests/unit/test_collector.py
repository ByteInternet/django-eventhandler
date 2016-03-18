import collections
from unittest import TestCase

import eventhandler
from eventhandler import handles_event, Dispatcher


class TestEventsCollector(TestCase):

    def setUp(self):
        eventhandler.HANDLERS = collections.defaultdict(list)

    def test_decorator_collects_handler(self):
        @handles_event('my_event')
        def my_handler():
            pass

        self.assertItemsEqual(Dispatcher().handlers['my_event'], [my_handler])

    def test_decorator_collects_multiple_events(self):
        @handles_event('my_event')
        @handles_event('my_other_event')
        def my_handler():
            pass

        self.assertItemsEqual(Dispatcher().handlers['my_event'], [my_handler])
        self.assertItemsEqual(Dispatcher().handlers['my_other_event'], [my_handler])

    def test_decorator_collects_multiple_handlers_for_same_event(self):
        @handles_event('my_event')
        def my_handler():
            pass

        @handles_event('my_event')
        def my_other_handler():
            pass

        self.assertEqual(Dispatcher().handlers['my_event'], [my_handler, my_other_handler])
