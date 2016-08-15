from django.db import models

from common.models import Entity, Relationship, BaseTreeModel

from common.choices import SexType
from user.choices import UserVerifyStatus


class User(Entity):
    mobile_phone = models.CharField(max_length = 16, db_index = True, unique = True)
    password     = models.CharField(max_length = 256)

    share_token = models.CharField(max_length = 128, db_index = True, unique = True)
    join_token  = models.CharField(max_length = 128, db_index = True, \
                  unique = True, null = True)

    verify_status = models.CharField(max_length = 256, \
                    default = UserVerifyStatus.initial)

    enable     = models.BooleanField(default = True)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'tb_user'
        ordering = ["uid"]


# 1 : 1
class UserInfo(Relationship):
    user = models.OneToOneField("User", to_field = "uid", 
           db_column = "user_uid", db_index = True, unique = True)

    # nickname = models.CharField(max_length = 256, null = True)
    # email    = models.CharField(max_length = 64, null = True)
    sex      = models.CharField(max_length = 32, default = SexType.unknown)
    avatar   = models.TextField(null = True)

    school    = models.TextField(null = True)
    college   = models.TextField(null = True)
    grade     = models.TextField(null = True)
    class_num = models.TextField(null = True)

    # is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'tb_user_info'
        ordering = ["uid"]


# 1 : 1
class UserIdentity(Relationship):
    user = models.OneToOneField("User", to_field = "uid", 
           db_column = "user_uid", db_index = True)

    id_name   = models.CharField(max_length = 256, null = True)
    id_number = models.CharField(max_length = 64, null = True)
    id_photos = models.TextField(null = True) # json list

    # is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'tb_user_identity'
        ordering = ["uid"]


# 1 : n
class UserBankAccount(Relationship):
    user = models.ForeignKey("User", to_field = "uid", 
           db_column = "user_uid", db_index = True)

    bank_name = models.TextField(null = True)
    # bank_type = models.CharField(max_length = 32, null = True)
    fee_type  = models.CharField(max_length = 32, default = 'CNY')

    account_name   = models.TextField(null = True)
    account_number = models.CharField(max_length = 64, null = True)

    card_photos = models.TextField(null = True) # json list

    enable = models.BooleanField(default = False)

    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'tb_user_bank_account'
        ordering = ["uid"]


# 1 : 1
class UserTree(BaseTreeModel):
    user = models.OneToOneField("User", to_field = "uid", 
           db_column = "user_uid", db_index = True)

    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class MPTTMeta:
        order_insertion_by = ['user']

    class Meta:
        db_table = 'tb_user_tree'
        ordering = ["uid"]


# class UserGroup(Relationship):
#     user = models.ForeignKey("User", to_field = "uid", 
#            db_column = "user_uid", db_index = True)

#     enable = models.BooleanField(default = False)

#     is_deleted = models.BooleanField(default = False)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
    
#     class Meta:
#         db_table = 'tb_user_group'
#         ordering = ["uid"]



