# -*- coding: utf-8 -*-
# import datetime
# import json
# import random
# import urllib
# import urllib2

# from django.conf import settings
# from django.db.models import Count

# from common.utils import get_cache, set_cache, delete_cache,\
#                          get_cache_dct, set_cache_dct, delete_cache_dct

# from user.models import UserCollectionProduct


# --------------------------------------------------------
# Basic
# --------------------------------------------------------

# def get_request_url(key):
#     return settings.PRODUCT_API.get(key, {}).get('url', 'None')


# def request_data(model, key=None, params=None):
#     base_url = settings.MANAGE_BACKEND_BASE_URL
#     url      = get_request_url(model)

#     if url.startswith('/'):
#         req_url = base_url + url
#     else:
#         req_url = '/'.join((base_url, url))

#     # All request will send as GET request
#     # E.g. 'http://192.168.100.3/products/1'
#     if key:
#         req_url = '/'.join((req_url, str(key)))

#     if params:
#         params = urllib.urlencode(params)
#         req_url = '?'.join((req_url, str(params)))

#     # request manage backend need token
#     token = get_manage_backend_token()
#     auth_key = 'Authorization'
#     auth_val = 'Bearer ' + str(token)

#     # Everything is ready. GO!
#     try:
#         # response = urllib.urlopen(req_url)
#         request = urllib2.Request(req_url)
#         request.add_header(auth_key, auth_val)

#         response = urllib2.urlopen(request)
#         content  = response.read()
        
#     # except urllib2.URLError as e:
#     except Exception as e:
#         # content = [{'data' : {'http_code' : e.code,
#         #                       'value'     : e.reason,
#         #                       'message'   : e.read()
#         #                      }
#         #            }]
#         content = []

#     try:
#         data = json.loads(content)
#     except:
#         data = content

#     return data


# def get_product_cache_key(key):
#     return 'product' + ':' + str(key)


# def get_product_cache_data(key):
#     ckey = get_product_cache_key(key)
#     data = get_cache(ckey)

#     return data


# def set_product_cache_data(key, data, expire=None):
#     ckey = get_product_cache_key(key)

#     set_cache(ckey, data, expire)

#     return data


# --------------------------------------------------------
# Func
# --------------------------------------------------------

# def get_product_data(key = None):
#     data = get_product_cache_data(key)

#     if not data:
#         if key:
#             data = request_data(model = 'products', key = key)
#             # If product_id not available, maybe return string:'404 Not Found'

#             # if not isinstance(data, dict):
#             #     data = {}
                
#             # data = [data]

#             # set_product_cache_data(key, data, \
#             #     expire = settings.PRODUCT_DATA_EXPIRE_SECONDS)

#             if isinstance(data, dict):
#                 data = [data]

#                 set_product_cache_data(key, data, \
#                     expire = settings.PRODUCT_DATA_EXPIRE_SECONDS)
#             else:
#                 data = []

#         else:
#             data = []

#     return data


# def get_products_data():
#     key  = 'products'
#     data = get_product_cache_data(key)

#     if not data:
#         data = request_data(model = 'products')

#         if isinstance(data, list):
#             set_product_cache_data(key, data, \
#                 expire = settings.PRODUCT_DATA_EXPIRE_SECONDS)
#         else:
#             data = []

#     return data


# def get_product_categories_data():
#     key  = 'categories'
#     data = get_product_cache_data(key)

#     if not data:
#         data = request_data(model = 'product_categories')

#         if isinstance(data, dict):
#             set_product_cache_data(key, data, \
#                 expire = settings.PRODUCT_DATA_EXPIRE_SECONDS)
#         else:
#             data = []

#     return data


# def get_product_data_with_params(params_dct):
#     # dct : {'departure': ..., 'destination':...}
#     # departure = dct.get('departure', None)
#     # destination = dct.get('destination', None)

#     # data_dep = []
#     # data_des = []

#     # if departure:
#     #     ckey_dep = 'region_code' + ':' + 'departure' + ':' + str(departure)
#     #     data_dep = get_product_cache_data(ckey_dep) or []

#     # if destination:
#     #     ckey_des = 'region_code' + ':' + 'destination' + ':' + str(destination)
#     #     data_des = get_product_cache_data(ckey_des) or []

#     key  =  ','.join(['{0}:{1}'.format(key,value)\
#             for key,value in params_dct.items()])
#     data = get_product_cache_data(key)

#     if not data:
#         data = request_data(model = 'products', params = params_dct)

#         if isinstance(data, list):
#             set_product_cache_data(key, data, \
#                 expire = settings.PRODUCT_DATA_EXPIRE_SECONDS)
#         else:
#             data = []

#     return data


# def get_product_date_data(product_id):
#     product_id = str(product_id)

#     key = str(product_id) +  ':' + 'date'
#     data = get_product_cache_data(key)

#     if not data:
#         key = product_id + '/date'
#         data = request_data(model = 'products', key = key)

#         if data and isinstance(data, list):
#             set_product_cache_data(key, data, \
#                 expire = settings.PRODUCT_DATA_EXPIRE_SECONDS)
#         else:
#             data = []

#     return data


# def get_product_price_with_date(product_id, date):
#     product_id = str(product_id)
#     date = str(date)

#     key = product_id +  ':' + 'price' + ':' + date
#     data = get_product_cache_data(key)

#     if not data:
#         key = product_id + '/price/' + date
#         data = request_data(model = 'products', key = key)

#         if data and isinstance(data, dict):
#             set_product_cache_data(key, data, \
#                 expire = settings.PRODUCT_DATA_EXPIRE_SECONDS)
#         else:
#             data = []

#     return data


# def get_product_price_with_sku(product_id, date, sku):
#     product_id = str(product_id)
#     date = str(date)
#     sku = str(sku)
 
#     key = product_id +  ':' + 'price' + ':' + date + ':' + sku
#     data = get_product_cache_data(key)

#     if not data:
#         key = product_id + '/price/' + date + '/' + sku
#         data = request_data(model = 'products', key = key)

#         if data and isinstance(data, dict):
#             set_product_cache_data(key, data, \
#                 expire = settings.PRODUCT_DATA_EXPIRE_SECONDS)
#         else:
#             data = []

#     return data

