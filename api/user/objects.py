import json

from django.conf import settings
# from django.db import transaction

from common.objects import BaseCacheObject

from user.models import User, UserInfo, UserIdentity, UserBankAccount, UserTree


class UserCache(BaseCacheObject):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-02 by Garvey
    --------------------------------
    self.get_cache_data(key)
    self.set_cache_data(key, data, expire)
    self.delete_cache_data(key)
    """
    def __init__(self, user_uid):
        super(UserCache, self).__init__()
        self.key = str(user_uid)
        self.user_uid = str(user_uid)
        self.expire = settings.USER_CACHE_DATA_EXPIRE_SECONDS

    def get_info(self):
        data = self.get_cache_data(key = self.key) or {}

        if not data:
            user = User.objects.filter(uid = self.user_uid, enable = True).\
                   first()

            if user:
                user_info = UserInfo.objects.filter(user = user).first()
                user_idy  = UserIdentity.objects.filter(user = user).first()

                data = {
                    # 'user_uid' : self.user_uid,
                    'mobile_phone'  : user.mobile_phone,
                    'share_token'   : user.share_token,
                    'join_token'    : user.join_token,
                    'verify_status' : user.verify_status,

                    'sex'       : user_info.sex,
                    'avatar'    : user_info.avatar,
                    'school'    : user_info.school,
                    'college'   : user_info.college,
                    'grade'     : user_info.grade,
                    'class_num' : user_info.class_num,
                    
                    'id_name'   : user_idy.id_name,
                    'id_number' : user_idy.id_number,
                    'id_photos' : json.loads(user_idy.id_photos) \
                                  if user_idy.id_photos else None,
                }

                bank_accounts = []
                user_ba_lst = UserBankAccount.objects.\
                              values('bank_name', 'fee_type', 'account_name',\
                                     'account_number', 'card_photos').\
                              filter(user = user, is_deleted = False).\
                              order_by('-uid')

                for user_ba in user_ba_lst:
                    card_photos = json.loads(user_ba.get('card_photos', None)) \
                                  if user_ba.get('card_photos', None) else None

                    ba_dict = {
                        'bank_name'      : user_ba.get('bank_name', None),
                        'fee_type'       : user_ba.get('fee_type', None),
                        'account_name'   : user_ba.get('account_name', None),
                        'account_number' : user_ba.get('account_number', None),
                        'enable'         : user_ba.get('enable', None),
                        'card_photos'    : card_photos,
                    }

                    bank_accounts.append(ba_dict)

                data.setdefault('bank_accounts', bank_accounts)

                self.set_cache_data(key = self.key,  \
                    data = data, expire = self.expire)

        return data

    def update_info(self):
        self.delete_info()
        return True

    def delete_info(self):
        self.delete_cache_data(key = self.key)
        return True

    def get_simple_info(self):
        info = self.get_info()

        id_number = info.get('id_number', '') or ''
        id_number.replace(id_number[4:-4], '*' * len(id_number[4:-4]))

        info['id_number'] = id_number

        if info.has_key('id_photos'):
            info.pop('id_photos')

        raw_bank_accounts = info.get('bank_accounts', []) 
        new_bank_accounts = []

        for ba in raw_bank_accounts:
            account_number = ba.get('account_number', '') or ''
            account_number.replace(account_number[4:-4], '*' * len(account_number[4:-4]))

            ba['account_number'] = account_number

            if ba.has_key('card_photos'):
                ba.pop('card_photos')

            new_bank_accounts.append(ba)

        if new_bank_accounts:
            info['bank_accounts'] = new_bank_accounts

        return info


class UserTreeObj(BaseCacheObject):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-04 by Garvey
    --------------------------------
    self.get_cache_data(key)
    self.set_cache_data(key, data, expire)
    self.delete_cache_data(key)
    """
    def __init__(self, user_uid):
        super(UserTreeObj, self).__init__()
        self.key = str(user_uid)
        self.user_uid = str(user_uid)
        self.expire = settings.USER_CACHE_DATA_EXPIRE_SECONDS
        self.tree_node = UserTree.objects.filter(user = self.user_uid).first()

    def get_parent(self):
        if self.tree_node:
            return self.tree_node.parent

        return None

    def get_children(self):
        if self.tree_node:
            return self.tree_node.get_children()

        return None

    def format_node_data(self, ut_node):
        data = {}

        if ut_node:
            user = ut_node.user
            user_info = user.userinfo
            user_id = user.useridentity

            data = {
                'mobile_phone'  : user.mobile_phone,
                'verify_status' : user.verify_status,

                'id_name' : user_id.id_name,
                
                'avatar'  : user_info.avatar,

                'updated_at' : ut_node.updated_at,
            } 

        return data 

    def get_parent_data(self):
        parent = self.get_parent()

        return self.format_node_data(ut_node = parent)

    def get_children_data(self):
        children_lst = self.get_children()

        return [self.format_node_data(ut_node = child) for child in children_lst]

    # def delete_node(self):
    #     return True
