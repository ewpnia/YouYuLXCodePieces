# Base Middlewares

from django.http import QueryDict, HttpResponse, HttpResponseBadRequest,\
                        HttpResponseForbidden, HttpResponseNotFound,\
                        HttpResponseNotAllowed, HttpResponseGone,\
                        HttpResponseServerError, JsonResponse
from django.conf import settings

from common.http import HttpResponseUnauthorized, HttpResponseConflict
from common.exceptions import UnauthorizedError

import base64
import hashlib
import json
import logging
import re
from time import time
import traceback


# default middelwares order(top->bottom):

# PutOrDeleteMiddleware
# HTTPHeadersSetMiddleware
# APIVersionControlMiddleware
# WebHeadersMiddleware
# VerifySignatureMiddleware
# ExceptionHandlerMiddleware

class PutOrDeleteMiddleware(object):
    """
    Parse post data from PUT/DELETE method request
    """
    def process_request(self, request):
        method = request.META.get("REQUEST_METHOD", "").upper()
        if method not in ["PUT", r"DELETE"]:
            return None

        # content_type = request.META.get("CONTENT_TYPE", "")
        # if content_type.startswith("multipart/form-data"):
        #     request.POST, request._files = request.parse_file_upload(request.META, request)
        # elif content_type.startswith("application/x-www-form-urlencoded"):
        #     request.POST = QueryDict(request.body, encoding = request.encoding)
            
        # if method == "PUT":
        #     request.PUT = request.POST
        # elif method == "DELETE":
        #     request.DELETE = request.POST

        content_type = request.META.get("CONTENT_TYPE", "")
        
        if content_type.startswith("application/json"):
            try:
                params = json.loads(request.body)
                assert isinstance(params, dict)
            except:
                params = {}

            if method in ("PUT", "DELETE"):
                setattr(request, method, params)
        
        else:
            if method == "PUT":
                params = QueryDict(request.body, encoding = request.encoding)
                request.PUT = params
            elif method == "DELETE":
                request.DELETE = request.GET

        return None
        

class HTTPHeadersSetMiddleware(object):
    """
    Set request.headers.
    Django format HTTP Headers like 'Content_Type' as 
    'HTTP_CONTENT_TYPE' in request.META
    """
    def process_request(self, request):
        headers = {k.replace('HTTP_', '').lower() : v  \
                    for (k, v) in request.META.items() \
                    if k.startswith('HTTP_')}

        setattr(request, 'headers', headers)

        return None


class APIVersionControlMiddleware(object):
    """
    Get the api version in request url, if not match the version in settings, 
    return special code to remind client to update. 
    """
    def __init__(self):
        self.version = settings.API_VERSION
        self.pass_path = settings.VERSION_PASS_PATH

    def process_request(self, request):
        if request.path_info in self.pass_path:
            return None
            
        # /1.0/ts -> ['', '1.0', 'ts']
        raw_path = request.path_info.split('/')
        request_version = raw_path[1]

        # (Not float) or (Request API version < setting API version)
        if (re.match("^\d+?\.\d+?$", request_version) is None) \
            or (request_version < self.version):
            # return HttpResponse('API Version error.', status=401)
            return JsonResponse(data = {'code' : 2, 'msg' : 'API Version error.'})

        # /1.0/ts -> /ts
        raw_path.remove(request_version)
        request.path_info = '/'.join(raw_path)

        return None


class WebHeadersMiddleware(object):
    """
    Add web headers to response.
    """
    def __init__(self):
        # self.web_cid = settings.WEB_CLIENT_ID
        self.web_headers  = settings.WEB_HEADERS 

    def process_request(self, request):

        method = request.META.get("REQUEST_METHOD")

        if method == "OPTIONS":
            response = HttpResponse(status = 204)

            for k,v in self.web_headers.items():
                response[k] = v

            return response

        return None

    def process_response(self, request, response):
        origin = request.headers.get('origin', None)

        for k,v in self.web_headers.items():
            response[k] = v

        if origin:
            response['Access-Control-Allow-Origin'] = origin

        return response


class VerifySignatureMiddleware(object):
    """
    Verify signature.
    >>> vid == hashlib.md5("#".join([sid, client.SECRET_KEY, ts])).hexdigest()
    """
    def __init__(self):
        self.web_cid = settings.WEB_CLIENT_ID
        self.ios_cid = settings.IOS_CLIENT_ID
        self.android_cid = settings.ANDROID_CLIENT_ID
        self.server_cid = settings.SERVER_CLIENT_ID
        self.available_seconds = int(settings.TS_AVAILABLE_SECONDS)

    def process_request(self, request):
        try:
            exclude_path = settings.NO_VERIFY_PATH

            if exclude_path:
                no_verify = [r for r in exclude_path                  \
                             if re.search(r, request.path) is not None]

                if no_verify:
                    return None

            method = request.META.get("REQUEST_METHOD")
            
            if method == "GET":
                query = request.GET.copy()
            elif method == "POST":
                query = request.POST.copy()
            elif method == "PUT":
                query = request.PUT.copy()
            elif method == "DELETE":
                query = request.DELETE.copy()
        
            cid = query.get("cid", None) # client_id
            sid = query.get("sid", None)
            ts  = query.get("ts",  None)
            vid = query.get("vid", None)

            assert cid and sid and vid
            assert ts and ts.isdigit()

            if cid == self.web_cid:
                key = settings.WEB_SECRET_KEY
            elif cid == self.ios_cid:
                key = settings.IOS_SECRET_KEY
            elif cid == self.android_cid:
                key = settings.ANDROID_SECRET_KEY
            elif cid == self.server_cid:
                key = settings.SERVER_SECRET_KEY
            else:
                raise Exception

            # try:
            #     ts_int = int(ts)
            # except:
            #     ts_int = 0
                
            # ts_now = int(time())

            # assert (ts_int - self.available_seconds) <= ts_now <= (ts_int + self.available_seconds)

            hs = hashlib.md5("#".join((str(sid), key, str(ts)))).hexdigest()

            assert hs == vid

            return None

            # return None if hs == vid \
            #     else HttpResponseUnauthorized('Signature verify failed.')

        except Exception as e:
            return HttpResponse('Signature verify failed.', status=401)


class ExceptionHandlerMiddleware(object):
    """
    Exception handlers middleware. Use to handle all pre-define
    errors. Each error correspond to a HTTP/1.1 Status Code.
    """
    def __init__(self):
        self.response = {
            "400": HttpResponseBadRequest,
            "401": HttpResponseUnauthorized,
            "403": HttpResponseForbidden,
            "404": HttpResponseNotFound,
            "405": HttpResponseNotAllowed,
            "409": HttpResponseConflict,
            "410": HttpResponseGone,
            "500": HttpResponseServerError,
        }
        
    def process_exception(self, request, e):
        traceback.print_exc()
        
        if hasattr(e, "code"):
            code = str(e.code)  
            if code in self.response.keys():
                cls = self.response[code]
                resp = cls()

                if hasattr(e, "message"):
                    setattr(resp, "content", e.message)
                return resp
        else: 
            return HttpResponseServerError(str(e))

