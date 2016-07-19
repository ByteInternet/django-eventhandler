import logging

from amqpconsumer.events import EventConsumer
from django.db import close_old_connections
from django.conf import settings
from django.core.management import BaseCommand

from eventhandler import Dispatcher

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Listen to events from the message queue and dispatch them to the ' \
           'correct event handler'

    def handle(self, *args, **options):
        dispatcher = Dispatcher(before_handler=_before, error_on_missing_type=False, ignore_handler_exceptions=True)
        consumer = EventConsumer(settings.LISTENER_URL,
                                 settings.LISTENER_QUEUE,
                                 dispatcher.dispatch_event,
                                 exchange=settings.LISTENER_EXCHANGE,
                                 exchange_type=settings.LISTENER_EXCHANGE_TYPE,
                                 routing_key=settings.LISTENER_ROUTING_KEY)
        logger.info("Starting to consume events")
        consumer.run()


def _before():
    # Because the event_listener runs for a long time, after a while the db connection times out
    # and for some reason, Django fails to automatically reconnect. so in order to force a living
    # db connection each time an event handler is evaluated, we run db.close_old_connections which
    # closes stale connections. Django will then establish a new connection when a db call is made.
    close_old_connections()
