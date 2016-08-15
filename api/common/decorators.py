from django.conf import settings

from common.exceptions import UnauthorizedError


__all__ = [
    'require_login',
]

def require_login(func):
    def _wrapper(request, *args, **kwargs):
        
        if not request.session.has_key("user_uid"):
            raise UnauthorizedError('Unauthorized, user did not login.')

        return func(request, *args, **kwargs)
    return _wrapper

