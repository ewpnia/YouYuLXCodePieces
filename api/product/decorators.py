from django.conf import settings
# from django.http import JsonResponse

from common.exceptions import UnauthorizedError
# from common.utils import DefaultJSONEncoder

from user.choices import UserVerifyStatus
from user.objects import UserCache

__all__ = [
    'require_login_and_verified',
]

def require_login_and_verified(func):
    def _wrapper(request, *args, **kwargs):

        if not request.session.has_key("user_uid"):
            raise UnauthorizedError('Unauthorized, user did not login.')

        uc = UserCache(user_uid = request.session.get('user_uid'))

        verify_status = uc.get_info().get('verify_status', None)

        if verify_status != UserVerifyStatus.passed:
            # 30006 : "User's account has not passed verify.",
            kwargs.setdefault('code', 30006)

        return func(request, *args, **kwargs)
    return _wrapper

