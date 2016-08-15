# Base Exceptions
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import ValidationError
from django.db import IntegrityError, DatabaseError, ProgrammingError


class BadRequestError(Exception):
    """
    Corresponds to HTTP/1.1 Status Code: "400 Bad Request"
    """
    def __init__(self, message = ""):
        self.code = 400
        self.value = "Bad Request"
        self.message = message
    def __str__(self):
        return repr(self.value)


class UnauthorizedError(Exception):
    """
    Corresponds to HTTP/1.1 Status Code: "401 Unauthorized"
    """
    def __init__(self, message = ""):
        self.code = 401
        self.value = "Unauthorized"
        self.message = message
    def __str__(self):
        return repr(self.value)


class ForbiddenError(Exception):
    """
    Corresponds to HTTP/1.1 Status Code: "403 Forbidden"
    """
    def __init__(self):
        self.code = 403 
        self.value = "Forbidden"
    def __str__(self):
        return repr(self.value)


class NotFoundError(Exception):
    """
    Corresponds to HTTP/1.1 Status Code: "404 Not Found"
    """
    def __init__(self, message = ""):
        self.code = 404
        self.value = "Not Found"
        self.message = message
    def __str__(self):
        return repr(self.value)


class MethodNotAllowedError(Exception):
    """
    Corresponds to HTTP/1.1 Status Code: "405 Method Not Allowed"
    """
    def __init__(self, allowed_methods = ["GET"]):
        self.code = 405
        self.value = "Method Not Allowed"
        self.allowed_methods = allowed_methods
    def __str__(self):
        return repr(self.value)


class ConflictError(Exception):
    """
    Corresponds to HTTP/1.1 Status Code: "409 Conflict"
    """
    def __init__(self):
        self.code = 409
        self.value = "Conflict"
    def __str__(self):
        return repr(self.value)
        

class InternalServerError(Exception):
    """
    Corresponds to HTTP/1.1 Status Code: "500 Internal Server Error"
    """
    def __init__(self, message = ""):
        self.code = 500
        self.value = "Internal Server Error"
        self.message = message
    def __str__(self):
        return repr(self.value)


class ErrorException(Exception):
    def __init__(self, e):
        traceback.print_exc()

        if isinstance(e, AttributeError):
            raise InternalServerError('Server error: %s.' % e)

        elif isinstance(e, KeyError):
            raise BadRequestError('Missing param: %s.' % e)

        elif isinstance(e, ObjectDoesNotExist):
            raise NotFoundError('Obj does not exist: %s.' % e)

        elif isinstance(e, ValidationError):
            raise BadRequestError('Validating error: %s.' % e)

        elif isinstance(e, IndexError):
            raise NotFoundError('Not available data: %s.' % e)

        elif isinstance(e, IntegrityError):
            raise ConflictError('DB error: %s.' % e)

        elif isinstance(e, DatabaseError):
            raise ConflictError('DB error: %s.' % e)

        elif isinstance(e, ProgrammingError):
            raise ConflictError('DB error: %s.' % e)

        elif isinstance(e, ValueError):
            raise NotFoundError('Value Error: %s.' % e)

        elif isinstance(e, AssertionError):
            raise BadRequestError('Param error: %s.' % e)

        else:
            raise InternalServerError('Server error: %s.' % e.message)


