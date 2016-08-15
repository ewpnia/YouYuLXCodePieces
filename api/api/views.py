
from django.conf import settings
from django.utils.decorators import method_decorator

from common.decorators import require_login
from common.exceptions import ErrorException
from common.views import BaseView
from common.utils import genarate_timestamp

# ---------------------------------------------------
# Basic
# ---------------------------------------------------

class HomeView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-04-02
    Modify : 2016-04-02 by Garvey
    --------------------------------
    Supported methods: GET
    """
    def get(self, request, *args, **kwargs):
        """
        Params: None
        """
        try:
            return self.http_response("Welcome to %s" % settings.APP_NAME)
        except Exception as e:
            raise ErrorException(e)


class TimestampView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-04-02
    Modify : 2016-04-02 by Garvey
    --------------------------------
    Supported methods: GET
    """
    def get(self, request, *args, **kwargs):
        """
        Params: None
        """
        try:
            return self.http_response(genarate_timestamp())
        except Exception as e:
            raise ErrorException(e)


# ---------------------------------------------------
# Test
# ---------------------------------------------------

class TestView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2015-11-30
    Modify : 2015-11-30 by Garvey
    --------------------------------
    Supported methods: GET
    """
    def get(self, request, *args, **kwargs):
        """
        Params: None
        """
        try:
            # data = request.headers
            # data = request.GET
            # data = request.GET
            data = None

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)

    def post(self, request, *args, **kwargs):
        """
        Params: None
        """
        # GET_REQUIRE_PARAMS = ('user_uid', )
        # (user_uid, ) = self.require_params

        try:
            # data = request.headers
            # data = request.GET

            data = {}

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)

