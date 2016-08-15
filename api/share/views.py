
from django.conf import settings
# from django.db import transaction
from django.utils.decorators import method_decorator

from common.decorators import require_login
from common.exceptions import ErrorException
from common.views import BaseView

from user.objects import UserCache


# class ShareProductView(BaseView):
#     """
#     --------------------------------
#     Author : Garvey Ding
#     Created: 2016-06-29
#     Modify : 2016-06-29 by Garvey
#     --------------------------------
#     Supported methods: GET
#     """
#     @method_decorator(require_login)
#     def get(self, request, *args, **kwargs):
#         """
#         Params: 
#             product_id = request.GET.get('product_id', None)
#         """
#         try:
#             user_uid = request.session.get('user_uid')
#             product_id = request.GET.get('product_id', None)

#             u_obj  = UserCache(user_uid = user_uid)
#             u_info = u_obj.get_info()

#             # data = { 'share_url'   : settings.SHARE_PRODUCT_URL,
#             #          'share_token' : u_info.get('share_token', '') }

#             # http://.../product?product_id=[product_id]&st=[share_token]

#             url = settings.PRODUCT_INDEX_URL
#             data = {'url' : url}

#             return self.encode_json_response(code = 0, data = data)

#         except Exception as e:
#             raise ErrorException(e)

