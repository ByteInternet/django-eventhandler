from django.test import TestCase
from django.test.utils import override_settings
import mock
from importlib import import_module as real_import_module
from eventhandler import collect_handlers
from eventhandler.tests.unit.events_module1 import other_handler_from_module1, handler_from_module1
from eventhandler.tests.unit.events_module2 import handler_from_module2


class TestCollectorIntegration(TestCase):
    """
    Test all handlers are following the event structure:
      key: list(eventmethods)
    """
    def test_collector_can_load_all_collector(self):
        for key, handlers in collect_handlers().iteritems():
            for handler in handlers:
                self.assertTrue(callable(handler), "handler in %s is not callable" % key)


@override_settings(INSTALLED_APPS=('app1', 'app2'))
class TestCollector(TestCase):
    def setUp(self):
        self.module1 = real_import_module('..events_module1', __name__)
        self.module2 = real_import_module('..events_module2', __name__)
        self.module_skip = real_import_module('..events_module_skip', __name__)
        self.invalid_module = real_import_module('..invalid_events_module', __name__)

        mock_import = mock.patch('importlib.import_module')
        self.import_module = mock_import.start()
        self.addCleanup(mock_import.stop)

    def test_that_collector_collects_event_handlers(self):
        self.import_module.side_effect = [self.module1, self.module2]

        res = collect_handlers()

        self.assertEqual(res, {
            'some_event': [handler_from_module1, other_handler_from_module1, handler_from_module2],
            'other_event': [other_handler_from_module1],
            'strange_event': [handler_from_module2],
            'tuple_event': [handler_from_module2],
        })

    def test_that_collector_imports_the_right_modules(self):
        self.import_module.side_effect = [self.module1, self.module2]

        collect_handlers()

        self.import_module.assert_has_calls([mock.call('app1.events'),
                                             mock.call('app2.events')])

    def test_that_collector_skips_apps_without_events_module(self):
        self.import_module.side_effect = [ImportError, self.module1]

        res = collect_handlers()

        self.assertEqual(res, self.module1.HANDLERS)

    def test_that_collector_skips_modules_without_handlers(self):
        self.import_module.side_effect = [self.invalid_module, self.module1]

        res = collect_handlers()

        self.assertEqual(res, self.module1.HANDLERS)

    def test_that_collector_skips_event_when_handlers_are_not_defined_within_a_list(self):
        self.import_module.side_effect = [self.module_skip, self.module1]
        res = collect_handlers()

        self.assertEqual(res, self.module1.HANDLERS)
