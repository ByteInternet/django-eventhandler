from amqpconsumer.events import EventConsumer
from django.conf import settings
from django.core.management import BaseCommand
import logging
from eventhandler import Dispatcher

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Listen to events from the message queue and dispatch them to the ' \
           'correct event handler'

    def handle(self, *args, **options):
        dispatcher = Dispatcher()
        consumer = EventConsumer(settings.LISTENER_URL,
                                 settings.LISTENER_QUEUE,
                                 dispatcher.dispatch_event,
                                 exchange=settings.LISTENER_EXCHANGE,
                                 exchange_type=settings.LISTENER_EXCHANGE_TYPE,
                                 routing_key=settings.LISTENER_ROUTING_KEY)
        logger.info("Starting to consume events")
        consumer.run()
