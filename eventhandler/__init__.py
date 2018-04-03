import json
import logging
import six
from collections import defaultdict

from copy import deepcopy

logger = logging.getLogger(__name__)

HANDLERS = defaultdict(list)


class Dispatcher(object):
    """ Event dispatcher

    The dispatch_event method of this class takes an event and based
    on the type of event it sends it to all event handlers that are
    registered for the event.

    To register an event handler, decorate a function with the
    @handles_event decorator. Pass the type of event to the decorator
    that you want to register the handler for.
    The function (handler) should take an event (dict) as argument.
    """
    def __init__(self, before_handler=None, error_on_missing_type=True, ignore_handler_exceptions=False):
        self.handlers = HANDLERS
        self.before_handler = before_handler
        self.error_on_missing_type = error_on_missing_type
        self.ignore_handler_exceptions = ignore_handler_exceptions

        logger.debug("Registered the following event handlers:")
        for event, handlers in six.iteritems(self.handlers):
            modules = set(map(lambda fn: '%s.%s' % (fn.__module__, fn.__name__), handlers))
            logger.debug("%s: %s", event, ', '.join(modules))

    def dispatch_event(self, event):
        logger.debug("Data: %s" % event)

        try:
            event_type = event['type']
            logger.info("Got %s event", event_type)
        except KeyError:
            if self.error_on_missing_type:
                raise RuntimeError('Event has no type: %s' % event)
            else:
                logger.error('Event has no type: %s' % event)
            return

        if callable(self.before_handler):
            if self.ignore_handler_exceptions:
                try:
                    self.before_handler()
                except Exception:
                    logger.exception("Before-handler raised an exception on event '%s'" % json.dumps(event))
            else:
                # separate call, so we do not mess up the stacktrace with try and except
                self.before_handler()

        for handler in self.handlers.get(event_type, []):
            logger.debug('executing %s.%s for %s event' % (handler.__module__, handler.__name__, event_type))

            if self.ignore_handler_exceptions:
                try:
                    handler(deepcopy(event))
                except Exception:  # Catch'em all!
                    logger.exception('Event handler raised an exception on {} event'.format(event['type']))
                    logger.debug('Event data: {}'.format(json.dumps(event)))
            else:
                # separate call, so we do not mess up the stacktrace with try and except
                handler(deepcopy(event))


def handles_event(event_type):
    def wrap(f):
        HANDLERS[event_type].append(f)
        return f
    return wrap
