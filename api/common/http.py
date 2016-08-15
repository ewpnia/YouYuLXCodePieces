from django.http import HttpResponse


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class HttpResponseConflict(HttpResponse):
    status_code = 409
