
from django.conf import settings
# from django.db import transaction
from django.utils.decorators import method_decorator

from common.decorators import require_login
from common.exceptions import ErrorException
from common.views import BaseView

from order.objects import UserOrderObj


class UserOrderView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-29
    Modify : 2016-07-27 by Garvey
    --------------------------------
    Supported methods: GET
    """
    @method_decorator(require_login)
    def get(self, request, *args, **kwargs):
        """
        Get user order list
        
        Params: None
        """
        try:
            user_uid = request.session.get('user_uid')

            u_order = UserOrderObj(user_uid = user_uid)
            data = u_order.get_order_list() 

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)
