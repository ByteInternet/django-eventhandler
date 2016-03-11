import json
import logging

from collections import defaultdict
from django.db import close_old_connections

logger = logging.getLogger(__name__)

HANDLERS = defaultdict(list)


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
        self.handlers = HANDLERS

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


def handles_event(event_type):
    def wrap(f):
        HANDLERS[event_type].append(f)
        return f
    return wrap
