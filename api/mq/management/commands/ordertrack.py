
# ./manage ordertrack

import logging

# from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from mq.consumers import OrderTrackConsumer


class Command(BaseCommand):
    help = 'Start order track consumers.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            o_con = OrderTrackConsumer()
            o_con.start()

        except Exception as e:
            log = '[error]-{msg}'.format(msg = str(e))
            self.stderr.write('Error: %s' % log)


