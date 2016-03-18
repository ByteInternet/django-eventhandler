import json
import logging

from collections import defaultdict

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
    def __init__(self, before_handler=None, error_on_missing_type=True):
        self.handlers = HANDLERS
        self.before_handler = before_handler
        self.error_on_missing_type = error_on_missing_type

        logger.debug("Registered the following event handlers:")
        for event, handlers in self.handlers.iteritems():
            modules = set(map(lambda fn: fn.__module__, handlers))
            logger.debug("%s: %s", event, ', '.join(modules))

    def dispatch_event(self, event):
        try:
            event_type = event['type']
        except KeyError:
            if self.error_on_missing_type:
                raise RuntimeError('Event has no type: %s' % event)
            else:
                logging.error('Event has no type: %s' % event)
            return

        logging.info("Got %s event", event_type)

        if callable(self.before_handler):
            self.before_handler()

        for handler in self.handlers.get(event_type, []):
            try:
                handler(event)
            except Exception:  # Catch'em all!
                logger.exception("Event handler raised an exception on event '%s'" % json.dumps(event))


def handles_event(event_type):
    def wrap(f):
        HANDLERS[event_type].append(f)
        return f
    return wrap
