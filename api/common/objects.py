
from common.utils import get_cache, set_cache, delete_cache

class BaseCacheObject(object):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-03-21
    Modify : 2016-03-24 by Garvey
    --------------------------------
    """
    # def __init__(self):

    def get_cache_key(self, key):
        return self.__class__.__name__ + ':' + str(key)

    def get_cache_data(self, key):
        ckey = self.get_cache_key(key)
        data = get_cache(ckey)

        return data

    def set_cache_data(self, key, data, expire=None):
        ckey = self.get_cache_key(key)
        set_cache(ckey, data, expire)

        return data

    def delete_cache_data(self, key):
        ckey = self.get_cache_key(key)
        delete_cache(ckey)

        return True
