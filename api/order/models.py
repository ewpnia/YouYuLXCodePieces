from django.db import models
from common.models import Relationship


class UserOrder(Relationship):
    user = models.ForeignKey("user.User", to_field = "uid", 
                  db_column = "user_uid", db_index = True)

    order_uid  = models.CharField(max_length = 64, db_index = True)
    order_code = models.CharField(max_length = 64, db_index = True)

    platform = models.CharField(max_length = 64)
    types    = models.CharField(max_length = 64)

    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'tb_user_order'
        ordering = ["uid"]
