import re

from django.conf import settings
from django.utils.decorators import method_decorator

from common.exceptions import ErrorException
from common.views import BaseView
from common.utils import cal_offset_limit

from product.decorators import require_login_and_verified
from product.objects import ProductCache, ProductsCache, ProductCategoryCache,\
                            ProductDateCache, ProductPriceCache


class ProductView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-05 by Garvey
    --------------------------------
    Supported methods: GET
    """
    @method_decorator(require_login_and_verified)
    def get(self, request, *args, **kwargs):
        """
        Params: 
            * product_id  : ID of product.                  [Optional]

            * departure   : Code of departure region.       [Optional]
            * destination : Code of destination region.     [Optional]
            * category_id : ID of category.                 [Optional]
            * recommend   : Whether product is recommended. [Optional]
                            Choices are 'true' and 'false'.

            * day_count : Day count of product.             [Optional]
                          e.g. 'day_count=7' 'day_count=1,3'
                               'day_count=1,' 'day_count=,3'
            * tags      : Tags of product.                  [Optional]
                          e.g. 'tags=shenzhen' 'tags=shenzhen,hongkong'
            * name      : Name of product.                  [Optional]
                          e.g. 'name=name_1' 'name=name_1 name_2'

            * destination_region_type : Should be used with 'departure'.    [Optional]
            # Only one of 'destination' or 'destination_region_type' should be given.
            # Only 'destination' works if both are given.


            * index : Page index.            [Optional]
                      Start from 1.
            * size  : Page size.             [Optional]
            # Only does it work when index and size are both given.
        """
        try:
            if kwargs.has_key('code'):
                return self.encode_json_response(code = kwargs.get('code'))

            index = request.GET.get('index', None)
            size  = request.GET.get('size', None)
            offset, limit = cal_offset_limit(index = index, size = size)

            product_id = request.GET.get('product_id', None)

            # Filter products by keys
            filter_keys = ('departure', 'destination', 'category_id',
                           'recommend', 'day_count', 'tags', 'name',
                           'destination_region_type')
            filter_kv = {}

            for key in filter_keys:
                val = request.GET.get(key, None)

                if val:
                    filter_kv.setdefault(key, val)


            product_id  = request.GET.get('product_id', None)

            departure   = request.GET.get('departure', None)
            destination = request.GET.get('destination', None)
            category_id = request.GET.get('category_id', None)
            recommend   = request.GET.get('recommend', None)

            # Get product detail by id
            if product_id:
                assert product_id.isdigit(), 'product_id must be digits'

                p_obj = ProductCache(product_id)
                data  = p_obj.get_data_dict()

            # Get products list with filter key-values
            elif filter_kv:
                ps_obj = ProductsCache()
                data = ps_obj.get_data_list_with_params(params = filter_kv)
                data = list(data[offset:limit])

            # Get products list
            else:
                ps_obj = ProductsCache()
                data = ps_obj.get_data_list()
                data = list(data[offset:limit])

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)


class ProductCategoryView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-05 by Garvey
    --------------------------------
    Supported methods: GET
    """
    @method_decorator(require_login_and_verified)
    def get(self, request, *args, **kwargs):
        """
        Params: None
        """
        try:
            if kwargs.has_key('code'):
                return self.encode_json_response(code = kwargs.get('code'))

            pc_obj = ProductCategoryCache()
            data   = pc_obj.get_data_list()
            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)


class ProductDateView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-05 by Garvey
    --------------------------------
    Supported methods: GET
    """
    @method_decorator(require_login_and_verified)
    def get(self, request, *args, **kwargs):
        """
        Params: 
            * product_id  : ID of product.     [Required]
        """
        try:
            if kwargs.has_key('code'):
                return self.encode_json_response(code = kwargs.get('code'))

            product_id = request.GET.get('product_id', None)

            assert product_id and product_id.isdigit(),\
                'product_id must be digits'

            pd_obj = ProductDateCache(product_id = product_id)
            data   = pd_obj.get_data_list()

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)


class ProductPriceView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-05 by Garvey
    --------------------------------
    Supported methods: GET
    """
    @method_decorator(require_login_and_verified)
    def get(self, request, *args, **kwargs):
        """
        Params: 
            * product_id : ID of product.          [Required]
            * date       : Date of product.        [Required]
                           Format in 'YYYY-MM-DD'

            * sku : '1:1;2:3' -> '1%3A1%3B2%3A3'.   [Optional]
        """
        try:
            if kwargs.has_key('code'):
                return self.encode_json_response(code = kwargs.get('code'))

            product_id = request.GET.get('product_id', None)
            date = request.GET.get('date', None)
            sku  = request.GET.get('sku', None)

            assert product_id and product_id.isdigit(),\
                'product_id must be digits'
            assert date, 'date must be given'

            assert re.match(settings.DATE_PATTERN, date) is not None,\
                'date must be format in YYYY-MM-DD'

            pp_obj = ProductPriceCache(product_id = product_id, date = date)

            if sku:
                data = pp_obj.get_data_list_with_sku(sku = sku)
            else:
                data = pp_obj.get_data_dict()

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)

