from django.conf import settings
from django.core.management import BaseCommand
from events.consumer import EventConsumer
import logging
from eventhandler import Dispatcher


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Listen to events from the message queue and dispatch them to the ' \
           'correct event handler'

    def handle(self, *args, **options):
        dispatcher = Dispatcher()
        consumer = EventConsumer(settings.EVENT_QUEUE_URL, settings.EVENT_QUEUE_QUEUE,
                                 dispatcher.dispatch_event,
                                 exchange=settings.EVENT_QUEUE_EXCHANGE,
                                 exchange_type='topic',
                                 routing_key='#')
        logger.info("Starting to consume events")
        consumer.run()
