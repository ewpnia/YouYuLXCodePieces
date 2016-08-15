# Base Views
import ast
import json
import logging

from django.core.cache import caches
# from django.db import models
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from common.exceptions import ErrorException
from common.utils import DefaultJSONEncoder, model_to_dict

from msg.utils import get_code_msg


class BaseView(View):
    def __init__(self, **kwargs):
        super(BaseView, self).__init__(**kwargs)
        self.cache = caches["default"]
        self.pass_code = { 0 : 'ok', }
        self.logging_format = "%(asctime)-15s %(message)s"

    def json_response(self, res):
        return JsonResponse(data = res, encoder = DefaultJSONEncoder)

    def http_response(self, res):
        return HttpResponse(res)

    def format_res(self, code, data=None):
        code = int(code)
        msg  = get_code_msg(code)

        if code not in self.pass_code:

            logging.basicConfig(format = self.logging_format)

            log = '[CODE]-{code}, [MSG]-{msg}'.\
                  format(code = code, msg = msg)

            logging.warning('Code Error: %s', log) 

        res = {
            'code' : code,
            'msg'  : msg,
        }

        if data is not None:
            res.setdefault('data', data)

        return res

    def encode_json_response(self, code, data=None):
        res = self.format_res(code = code, data = data)
        return self.json_response(res = res)


class BaseCRUDView(BaseView):
    def get(self, request, *args, **kwargs):
        try:
            uid = kwargs.get('uid', None)

            if uid:
                obj = self.model.objects.get(uid = uid)
                data = model_to_dict(obj)
            else:
                dct = request.GET.dict()
                obj_lst = self.model.objects.filter(**dct)
                data = [model_to_dict(obj) for obj in obj_lst]

            if hasattr(self, 'json_encode_fields'):

                for field in self.json_encode_fields:
                    if data.has_key(field) and data[field]:
                        try:
                            data[field] = json.loads(data[field])
                        except:
                            data[field] = ast.literal_eval(data[field])

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)

    def post(self, request, *args, **kwargs):
        res = {'data' : 'In POST',}
        return self.json_response(res = res)

    def put(self, request, *args, **kwargs):
        res = {'data' : 'In PUT',}
        return self.json_response(res = res)

    def delete(self, request, *args, **kwargs):
        res = {'data' : 'In DELETE',}
        return self.json_response(res = res)

