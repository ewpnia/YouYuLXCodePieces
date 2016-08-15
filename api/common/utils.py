import datetime
import decimal
import json
import random
import socket
import string
import time
import urllib

from django.conf import settings
from django.core.cache import caches
from django.db.models import Model
from django.db.models.query import QuerySet
from django.db.models.fields.related import ManyToManyField

__all__ = [
    'model_to_dict',
    'clear_cache',
    'get_cache',
    'set_cache',
    'delete_cache',
    'get_cache_dct',
    'set_cache_dct',
    'delete_cache_dct',
    'get_enumerate_cache',
    'cal_offset_limit',
    'is_digits_split_by_dot',
    'is_valid_ip',
    'genarate_timestamp',
    'generate_random_string',
    'decode_unicode_param',
]

class DefaultJSONEncoder(json.JSONEncoder):
    # def __call__(self, o):
    def default(self, o):
        if isinstance(o, QuerySet):
            return [model_to_dict(m) for m in o]
        elif isinstance(o, Model):
            return model_to_dict(o)
        elif isinstance(o, decimal.Decimal):
            # return "%.4f" % o
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
            # return o.strftime("%Y-%m-%d %H:%M:%S UTC+0800")
            # return o.strftime("%Y-%m-%d %H:%M:%S.%f")
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, datetime.time):
            return o.strftime("%H:%M:%S")
        elif isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)


def model_to_dict(instance, fields=None, exclude=None):
    """
    Returns a dict containing the data in 'instance' suitable for passing as
    a Form's 'initial' keyword argument.

    'fields' is an optional list of field names. If provided, only the named
    fields will be included in the returned dict.

    'exclude' is an optional list of field names. If provided, the named
    fields will be excluded from the returned dict, even if they are listed in
    the 'fields' argument.
    """
    # opts = instance._meta
    # if instance._meta.db_table.model_name  == 'User'
    #     exclude = ['uid']
    if instance is None:
        return 'None'

    data = {}
    for f in instance._meta.fields:
        if fields and not f.name in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            # If the object doesn't have a primary key yet, just use an empty
            # list for its m2m fields. Calling f.value_from_object will raise
            # an exception.
            if instance.pk is None:
                data[f.name] = []
            else:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                qs = f.value_from_object(instance)
                if qs._result_cache is not None:
                    data[f.name] = [item.pk for item in qs]
                else:
                    data[f.name] = list(qs.values_list('pk', flat=True))
        else:
            k = f.db_column if f.db_column is not None else f.name
            data[k] = f.value_from_object(instance)
    return data


def cal_offset_limit(index = None, size = None):
    index = index or settings.DEFAULT_INDEX
    size  = size or settings.DEFAULT_SIZE

    # Calculate offset and limit with index and size
    if index:
        assert index.isdigit(), 'index must be digits'
        index = int(index)

    if size:
        assert size.isdigit(), 'size must be digits'
        size = int(size)

    if size and index:
        offset = (index - 1) * size
        limit  = index * size
    else:
        offset = None
        limit  = None

    return offset, limit


def is_digits_split_by_dot(string):
    char_set = set(string)

    for char in char_set:
        if not char.isdigit() and char != ',':
            return False

    return True

    
def is_valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False


def genarate_timestamp():
    return str(int(time.time()))


def generate_random_string(length):
    seed = string.letters + string.digits
    random_lst = [random.choice(seed) for i in xrange(length)]
    random.shuffle(random_lst)

    return ''.join(random_lst)


def decode_unicode_param(param):
    param = param.encode('ascii')
    param = urllib.unquote(param)
    param = param.decode('utf-8')

    return param


# ------------------------------------------------
# Cache related
# ------------------------------------------------

def clear_cache():
    cache = caches["default"]
    cache.clear()


def get_cache(key):
    cache = caches["default"]

    ckey = settings.CACHE_SCOPE_DELIMITER.join((settings.CACHE_KEY_PREFIX, key))
    data = cache.get(ckey, None)

    return data


def set_cache(key, data, expire=3600):
    cache = caches["default"]

    ckey = settings.CACHE_SCOPE_DELIMITER.join((settings.CACHE_KEY_PREFIX, key))
    cache.set(ckey, data, expire)

    return data


def delete_cache(key):
    cache = caches["default"]

    ckey = settings.CACHE_SCOPE_DELIMITER.join((settings.CACHE_KEY_PREFIX, key))
    cache.delete(ckey)

    return None


def get_cache_dct(key_lst):
    cache = caches["default"]

    ckey_lst = [settings.CACHE_SCOPE_DELIMITER.join((settings.CACHE_KEY_PREFIX, key)) \
                for key in key_lst]

    data = cache.get_many(ckey_lst, None)

    # Return an OrderedDict
    return data


def set_cache_dct(data_dct):
    cache = caches["default"]

    cache_data_dct = {}

    for key,value in data_dct.items():
        ckey = settings.CACHE_SCOPE_DELIMITER.join((settings.CACHE_KEY_PREFIX, key))
        cache_data_dct.setdefault(ckey, value)

    data = cache.set_many(cache_data_dct)

    return data


def delete_cache_dct(key_lst):
    cache = caches["default"]

    ckey_lst = [settings.CACHE_SCOPE_DELIMITER.join((settings.CACHE_KEY_PREFIX, key)) \
                for key in key_lst]

    data = cache.delete_many(ckey_lst, None)

    return data


def get_enumerate_cache(key):
    cache = caches["default"]

    ckey = settings.CACHE_SCOPE_DELIMITER.join((settings.CACHE_KEY_PREFIX, key))
    data = cache.get(ckey, None)

    if not data:
        data = 1
        cache.set(ckey, 2, None)
    else:
        cache.incr(ckey)

    return data



