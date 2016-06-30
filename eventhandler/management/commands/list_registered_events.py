import logging
from django.core.management import BaseCommand

from eventhandler import Dispatcher

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'List all currently registered events'

    def handle(self, *args, **options):
        dispatcher = Dispatcher()
        for event, handlers in sorted(dispatcher.handlers.iteritems()):
            self.stdout.write(event)
            readable_handlers = ["%s.%s" % (h.__module__, h.__name__) for h in handlers]

            for handler in sorted(readable_handlers):
                self.stdout.write("  - %s" % handler)
            self.stdout.write("")
