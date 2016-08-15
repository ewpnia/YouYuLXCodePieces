
RABBITMQ_HOST = 'localhost'

RABBITMQ_USER_ID = 'yylxuser'
RABBITMQ_USER_PW = 'com.youyulx.mq'

RABBITMQ_ORDER_TRACK_QUEUE_NAME = 'yylx.order.track.queue'

RABBITMQ_ORDER_EXCHANGE_NAME = 'yylx.order.exchange'

# RABBITMQ_EXCHANGE_TYPE_FANOUT = 'fanout'
RABBITMQ_EXCHANGE_TYPE_DIRECT = 'direct'

# routing_key format 'aaa.bbb.ccc'
# routing_key can be ['test.yylx', ...], queue_bind with for
RABBITMQ_ORDER_ROUTING_KEY = 'yylx.order.route'

