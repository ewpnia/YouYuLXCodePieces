import requests
import urllib

from django.conf import settings
from django.db import transaction

from common.objects import BaseCacheObject


class ProductBaseCache(BaseCacheObject):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-06-28 by Garvey
    --------------------------------
    self.get_cache_data(key)
    self.set_cache_data(key, data, expire)
    self.delete_cache_data(key)
    """
    def __init__(self):
        super(ProductBaseCache, self).__init__()
        self.expire = settings.PRODUCT_DATA_EXPIRE_SECONDS
        self.ckey = None
        self.url_key = None

    def get_request_url(self):
        base_url = settings.MANAGE_BACKEND_BASE_URL
        url = settings.PRODUCT_API.get(self.url_key, {}).get('url', 'None')

        req_url = base_url + url if url.startswith('/') else \
                  '/'.join((base_url, url))

        return req_url

    def format_restful_url(self):
        return self.get_request_url()

    # For list data
    def get_data_list(self):
        data = self.get_cache_data(key = self.ckey) or []

        if not data:
            url = self.format_restful_url()

            r = requests.get(url)

            try:
                data = r.json() or []
            except:
                data = []

            if data:
                self.set_cache_data(key = self.ckey, \
                    data = data, expire = self.expire)

        return data

    def update_data_list(self):
        self.delete_data_list()
        return True

    def delete_data_list(self):
        self.delete_cache_data(key = self.ckey)
        return True

    # For dict data
    def get_data_dict(self):
        data = self.get_cache_data(key = self.ckey) or {}

        if not data:
            url = self.format_restful_url()

            r = requests.get(url)

            try:
                data = r.json() or {}
            except:
                data = {}

            if data:
                self.set_cache_data(key = self.ckey, \
                    data = data, expire = self.expire)

        return data

    def update_data_dict(self):
        self.delete_data_dict()
        return True

    def delete_data_dict(self):
        self.delete_cache_data(key = self.ckey)

        return True


class ProductCache(ProductBaseCache):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-06-28 by Garvey
    --------------------------------
    self.get_cache_data(key)
    self.set_cache_data(key, data, expire)
    self.delete_cache_data(key)
    """
    def __init__(self, product_id):
        super(ProductCache, self).__init__()
        self.ckey = str(product_id)
        self.product_id = str(product_id)
        self.url_key = 'products'

    def format_restful_url(self):
        url = self.get_request_url()
        return '/'.join((url, self.product_id))


class ProductsCache(ProductBaseCache):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-06-28 by Garvey
    --------------------------------
    self.get_cache_data(key)
    self.set_cache_data(key, data, expire)
    self.delete_cache_data(key)
    """
    def __init__(self):
        super(ProductsCache, self).__init__()
        self.ckey = 'products'
        self.url_key = 'products'

    def get_data_list_with_params(self, params):
        url = self.get_request_url()

        r = requests.get(url, params = params)

        try:
            data = r.json() or []
        except:
            data = []

        return data


class ProductCategoryCache(ProductBaseCache):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-06-28 by Garvey
    --------------------------------
    self.get_cache_data(key)
    self.set_cache_data(key, data, expire)
    self.delete_cache_data(key)
    """
    def __init__(self):
        super(ProductCategoryCache, self).__init__()
        self.ckey = 'product_categories'
        self.url_key = 'product_categories'


class ProductDateCache(ProductBaseCache):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-06-28 by Garvey
    --------------------------------
    self.get_cache_data(key)
    self.set_cache_data(key, data, expire)
    self.delete_cache_data(key)
    """
    def __init__(self, product_id):
        super(ProductDateCache, self).__init__()
        self.ckey = str(product_id)
        self.product_id = str(product_id)
        self.url_key = 'products'
        self.child_url = 'date'

    def format_restful_url(self):
        url = self.get_request_url()
        # http://172.18.0.1:6543/product/products/255/date
        return '/'.join((url, self.product_id, self.child_url))


class ProductPriceCache(ProductBaseCache):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-06-28 by Garvey
    --------------------------------
    self.get_cache_data(key)
    self.set_cache_data(key, data, expire)
    self.delete_cache_data(key)
    """
    def __init__(self, product_id, date):
        super(ProductPriceCache, self).__init__()
        self.ckey = str(product_id) + ':' + str(date)
        self.product_id = str(product_id)
        self.date = str(date)
        self.url_key = 'products'
        self.child_url = 'price'

    def format_restful_url(self):
        url = self.get_request_url()

        # http://172.18.0.1:6543/product/products/255/price/2016-06-28

        return '/'.join((url, self.product_id, self.child_url, self.date))

    def get_data_list_with_sku(self, sku):
        sku = urllib.unquote(sku)

        # http://172.18.0.1:6543/product/products/255/price/2016-06-28/1:1;2:2
        url = self.format_restful_url() + '/' + sku

        r = requests.get(url)

        try:
            data = r.json() or []
        except:
            data = []

        return data


        