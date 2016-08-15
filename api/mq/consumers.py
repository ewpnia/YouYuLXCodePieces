
import pika
import json
import logging

from django.conf import settings
# from django.db import transaction, connection
# from django.db.models import F, Max, Q, Sum, Count
# from django.utils.decorators import method_decorator

# from common.decorators import require_login
# from common.exceptions import ErrorException
# from common.views import BaseView
# from common.utils import model_to_dict, clear_cache, get_cache,\
#                          set_cache, delete_cache, http_request, cal_offset_limit,\
#                          genarate_timestamp

from order.objects import UserOrderObj


class BaseConsumer(object):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-07-23
    Modify : 2016-07-25 by Garvey
    --------------------------------
    """
    def __init__(self):
        self.host = ''
        self.user_id = ''
        self.user_pw = ''

        self.queue_name    = ''
        self.exchange_name = ''
        self.exchange_type = ''
        self.routing_key   = ''

        self.delivery_mode = 2 # Make message persistent
        self.content_type  = 'application/json'

        # This tells RabbitMQ not to give 
        # more than one message to a worker at a time.
        self.prefetch_count = 1

        self.logging_format = "%(asctime)-15s %(message)s"

    def _set_channel(self):
        credentials = pika.PlainCredentials(self.user_id, self.user_pw)
        parameters  = pika.ConnectionParameters(credentials = credentials,
                                                       host = self.host)
        connection  = pika.BlockingConnection(parameters)
        channel     = connection.channel()

        channel.exchange_declare(exchange = self.exchange_name,
            type = self.exchange_type, durable = True)
        channel.queue_declare(queue = self.queue_name, durable = True)
        channel.queue_bind(exchange = self.exchange_name, queue = self.queue_name,
                                                    routing_key = self.routing_key)

        setattr(self, 'channel', channel)

    def __callback(self, ch, method, properties, body):
        # print 'method.exchange', method.exchange
        # print 'method.redelivered', method.redelivered
        # print 'method.routing_key', method.routing_key

        # print 'properties.content_type', properties.content_type
        # print 'properties.delivery_mode', properties.delivery_mode
        # print 'properties.reply_to', properties.reply_to

        # logging.basicConfig(format = self.logging_format)

        # log = '[method]-{method}, [properties]-{properties}'.\
        #       format(method = repr(method), properties = repr(properties))

        # logging.warning('Callback: %s', log)

        self.process_body(body = body)

        ch.basic_ack(delivery_tag = method.delivery_tag)

    def process_body(self, body):
        return True

    def start(self):
        self.channel.basic_qos(prefetch_count = self.prefetch_count)

        # If no_ack == True, message acknowledgments are turned off
        # channel.basic_consume(callback, queue = 'hello', no_ack = True)
        self.channel.basic_consume(self.__callback, queue = self.queue_name)

        self.channel.start_consuming()


class OrderTrackConsumer(BaseConsumer):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-07-23
    Modify : 2016-07-23 by Garvey
    --------------------------------
    """
    def __init__(self):
        super(OrderTrackConsumer, self).__init__()
        self.host = settings.RABBITMQ_HOST
        self.user_id = settings.RABBITMQ_USER_ID
        self.user_pw = settings.RABBITMQ_USER_PW

        self.queue_name    = settings.RABBITMQ_ORDER_TRACK_QUEUE_NAME
        self.exchange_name = settings.RABBITMQ_ORDER_EXCHANGE_NAME
        self.exchange_type = settings.RABBITMQ_EXCHANGE_TYPE_DIRECT
        self.routing_key   = settings.RABBITMQ_ORDER_ROUTING_KEY

        self._set_channel()

    def process_body(self, body):
        try:
            body = json.loads(body)
        except:
            body = None

        logging.basicConfig(format = self.logging_format)
        log = '[body]-{body}'.format(body = body)
        logging.warning('Callback: %s', log)

        share_token = body.get('share_token', None)
        order_uid   = body.get('order_uid', None)
        order_code  = body.get('order_code', None)
        platform    = body.get('platform', None)
        types       = body.get('types', None)

        u_order = UserOrderObj(share_token = share_token)

        params_ok = u_order.ensure_create_params(order_uid = order_uid, 
                         order_code = order_code, platform = platform, types = types)

        if params_ok:
            u_order.create(order_uid = order_uid, order_code = order_code, 
                            platform = platform, types = types)

        return True

