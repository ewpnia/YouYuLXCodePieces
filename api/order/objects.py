import json
import requests
import urllib

from django.conf import settings
# from django.db import transaction

# from common.objects import BaseCacheObject

from order.choices import OrderPlatform, OrderTypes
from order.models import UserOrder

from user.models import User


class UserOrderObj(object):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-07-22
    Modify : 2016-07-25 by Garvey
    --------------------------------
    """
    def __init__(self, user_uid=None, share_token=None):
        self.user_uid = user_uid
        self.share_token = share_token
        # self.platform = ''
        # self.types = ''
        self.order_req_url = settings.ORDER_BASE_URL + settings.ORDER_URL

    def ensure_create_params(self, order_uid, order_code, platform, types):
        if order_uid and order_code and platform and types:
            if not str(order_uid).isdigit():
                return False

            if platform not in OrderPlatform.__dict__.keys() or platform.startswith('__'):
                return False

            if types not in OrderTypes.__dict__.keys() or types.startswith('__'):
                return False

            return True

        else:
            return False

    def create(self, order_uid, order_code, platform, types):
        created = None

        if self.share_token:
            user = User.objects.filter(share_token = self.share_token, enable = True).\
                   first() 

            if user:
                u_order, created = UserOrder.objects.get_or_create(
                                       order_uid = order_uid,
                                       defaults = {
                                           'user'       : user, 
                                           'order_code' : order_code, 
                                           'platform'   : platform,
                                           'types'      : types,
                                       }
                                   )

        return created

    def get_order_list(self):
        order_uid_list = UserOrder.objects.\
                         values_list('order_uid', flat = True).\
                         filter(user = self.user_uid, is_deleted = False).\
                         order_by('-created_at')
                          
        params = {'order_uid_list' : json.dumps(list(order_uid_list))}

        r = requests.get(self.order_req_url, params = params)

        try:
            res = r.json() or {}
        except:
            res = {}

        data = res.get('data', []) 

        return data

