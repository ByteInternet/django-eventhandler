from collections import defaultdict
import importlib
import json
import logging
from django.conf import settings
from django.db import close_old_connections

logger = logging.getLogger(__name__)

EVENTS_MODULE_NAME = 'events'
EVENTS_HANDLERS_NAME = 'HANDLERS'


class Dispatcher(object):
    """ Event dispatcher

    The dispatch_event method of this class takes an event and based
    on the type of event it sends it to all event handlers that are
    registered for the event.

    To register an event handler, create a file called `events.py` in
    your installed app and have it contain a dict called HANDLERS which
    maps event names to a list of functions that take an event (dict)
    as first argument.
    """

    def __init__(self):
        self.handlers = collect_handlers()

        logger.debug("Registered the following event handlers:")
        for event, handlers in self.handlers.iteritems():
            modules = set(map(lambda fn: fn.__module__, handlers))
            logger.debug("%s: %s", event, ', '.join(modules))

    def dispatch_event(self, event):
        event_type = event.get('type')
        logging.info("Got %s event", event_type)
        handlers = self.handlers.get(event_type, [])
        for handler in handlers:
            try:
                # Because the event_listener runs for a long time, after a while the db connection times out
                # and for some reason. (this version of?) Django fails to automatically reconnect. so in order
                # to force a living db connection each time an event handler is evaluated, we run
                # db.close_old_connections which closes stale connections. django will then establish a new
                # connection when a db call is made.
                close_old_connections()
                handler(event)
            except Exception:  # Catch'em all!
                logger.exception("Event handler raised an exception on event '%s'" % json.dumps(event))


def collect_handlers():
    """
    Collect event handlers of all installed apps.
    Ignore and skip misconfigured eventshandlers.
    """

    handlers = defaultdict(list)
    for app in settings.INSTALLED_APPS:
        try:
            module = importlib.import_module('%s.%s' % (app, EVENTS_MODULE_NAME))
        except ImportError:
            continue

        handlercoll = getattr(module, EVENTS_HANDLERS_NAME, {})
        for event, hs in handlercoll.iteritems():
            try:
                _verify_handlers(event=event, handlers=hs)
                handlers[event] += hs
            except:
                logger.exception("eventhandler '%s' will be skipped due misconfiguration" % event)
    return handlers


def _verify_handlers(event, handlers):
    if not all(callable(method) for method in handlers):
        raise ValueError('%s Does not contain callables' % event)
