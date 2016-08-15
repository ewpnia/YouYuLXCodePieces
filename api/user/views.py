import datetime
import json

from django.conf import settings
from django.db import transaction
from django.utils.decorators import method_decorator

from common.decorators import require_login
from common.exceptions import ErrorException
from common.views import BaseView
from common.utils import get_cache, delete_cache, cal_offset_limit,\
                         decode_unicode_param
from common.choices import SexType, IDType

from user.utils import generate_db_pw, mobile_phone_is_available,\
                       id_number_is_available, generate_share_token, generate_join_token

from user.choices import UserVerifyStatus
from user.models import User, UserInfo, UserIdentity, UserBankAccount, UserTree
from user.objects import UserCache, UserTreeObj


class UserRegisterView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-02 by Garvey
    --------------------------------
    Supported methods: POST
    """
    def post(self, request, *args, **kwargs):
        """
        Params: 
            * mobile_phone : Mobile phone number.  [Required]
            * password     : Password.             [Required]
            * sms_code     : SMS Code.             [Required]
            * join_token   : Parent's join_token.  [Optional]
        """
        try:
            mobile_phone = request.POST.get('mobile_phone', None)
            password     = request.POST.get('password', None)
            sms_code     = request.POST.get('sms_code', None)
            join_token   = request.POST.get('join_token', None)

            assert mobile_phone and mobile_phone.isdigit(),\
                'mobile_phone is required and must be digits'
            assert password, 'password is required'
            # assert join_token, 'join_token is required'
            assert sms_code and sms_code.isdigit(), \
                'sms_code is required and must be digits'

            assert mobile_phone_is_available(mobile_phone),\
                'mobile_phone is not available'

            code = 0

            cache_key = 'sms_code' + mobile_phone
            # cache_sms_code = get_cache(cache_key)
            cache_sms_code = sms_code

            if cache_sms_code != sms_code:
                # SMS code verify error.
                code = 30101

            elif User.objects.\
                filter(mobile_phone = mobile_phone, enable = True).exists():
                    # Account exists.
                    code = 30001

            if join_token and code == 0:
                # parent join_token is exists and parent has passed verify
                parent_user = User.objects.\
                              select_related('usertree').\
                              filter(join_token = join_token,\
                                    verify_status = UserVerifyStatus.passed,\
                                    enable = True).\
                              first()

                if not parent_user:
                    code = 30004 # Join token is not available.

                else:
                    parent_level = parent_user.usertree.level

                    if parent_level >= settings.USER_TREE_MAX_LEVEL:
                        code = 30005  # Parent's level reach limit, can't have children.

            if code == 0:
                # SMS Code right and user not exists
                hash_pw = generate_db_pw(org_pw = password,   \
                                   mobile_phone = mobile_phone)

                share_token  = generate_share_token()
                u_join_token = generate_join_token()

                delete_cache(cache_key)

                with transaction.atomic():
                    user = User.objects.create(                                 \
                            mobile_phone = mobile_phone, password = hash_pw,    \
                            share_token = share_token, join_token = u_join_token)

                    UserInfo.objects.create(user = user)
                    UserIdentity.objects.create(user = user)

                    if join_token:
                        UserTree.objects.create(user = user,\
                                                parent = parent_user.usertree)

                    else:
                        UserTree.objects.create(user = user)
                        

            return self.encode_json_response(code = code)

        except Exception as e:
            raise ErrorException(e)


class UserLoginView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-02 by Garvey
    --------------------------------
    Supported methods: POST
    """
    def post(self, request, *args, **kwargs):
        """
        Params: 
            * mobile_phone : Mobile phone number.  [Required]
            * password     : Password.             [Required]
        """
        try:
            mobile_phone = request.POST.get('mobile_phone')
            password     = request.POST.get('password')

            assert mobile_phone and mobile_phone.isdigit(), \
                'mobile_phone is required and must be digits'
            assert password, 'password is required'

            assert mobile_phone_is_available(mobile_phone), \
                'mobile_phone is not available'

            code = 0
            data = {}

            hash_pw = generate_db_pw(org_pw = password,   \
                               mobile_phone = mobile_phone)

            user = User.objects.filter(mobile_phone = mobile_phone, \
                         password = hash_pw, enable = True).\
                   first()

            if not user:
                # Login failed
                # Mobile phone number or password error.
                code = 30002

            else:
                user_uid = str(user.uid)

                request.session['user_uid'] = user_uid

                u_cache = UserCache(user_uid = user_uid)
                data = u_cache.get_simple_info()
                
            return self.encode_json_response(code = code, data = data)

        except Exception as e:
            raise ErrorException(e)


class UserChangePWView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-02 by Garvey
    --------------------------------
    Supported methods: PUT
    """
    def put(self, request, *args, **kwargs):
        """
        Params: 
            * mobile_phone : Mobile phone number.  [Required]
            * password     : New password.         [Required]
            * sms_code     : SMS Code.             [Required]
        """
        try:
            mobile_phone = request.PUT.get('mobile_phone')
            password = request.PUT.get('password')
            sms_code = request.PUT.get('sms_code')

            assert mobile_phone and mobile_phone.isdigit(),\
                'mobile_phone is required and must be digits'
            assert sms_code and sms_code.isdigit(), \
                'sms_code is required and must be digits'
            assert password, 'password is required'

            assert mobile_phone_is_available(mobile_phone), \
                'mobile_phone is not available'

            code = 0

            cache_key = 'sms_code' + mobile_phone
            # cache_sms_code = get_cache(cache_key)
            cache_sms_code = sms_code

            if cache_sms_code != sms_code:
                # SMS code verify error.
                code = 30101

            else:
                delete_cache(cache_key)
                
                hash_pw = generate_db_pw(org_pw = password,   \
                                   mobile_phone = mobile_phone)

                updated = User.objects.filter(mobile_phone = mobile_phone,\
                                                    enable = True).\
                          update(password = hash_pw,\
                                 updated_at = datetime.datetime.now())

                if not updated:
                    # Account not exists.
                    code = 30003

            return self.encode_json_response(code = code)

        except Exception as e:
            raise ErrorException(e)


class UserLogoutView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-06-28 by Garvey
    --------------------------------
    Supported methods: POST
    """
    @method_decorator(require_login)
    def post(self, request, *args, **kwargs):
        """
        Params: None
        """
        try:
            # user_uid = request.session.get('user_uid')

            # request.session.clear()
            request.session.flush()

            return self.encode_json_response(code = 0)

        except Exception as e:
            raise ErrorException(e)


class UserInfoView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-06-28
    Modify : 2016-07-02 by Garvey
    --------------------------------
    Supported methods: GET, POST
    """
    @method_decorator(require_login)
    def get(self, request, *args, **kwargs):
        """
        Params : None
        """
        try:
            user_uid = request.session.get('user_uid')

            u_obj = UserCache(user_uid = user_uid)
            data  = u_obj.get_info()

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)

    @method_decorator(require_login)
    def post(self, request, *args, **kwargs):
        """
        Create or update user info.

        Params : 
            * sex       : User's sex.           [Optional]
            * avatar    : URL of user's avatar. [Optional]
            * school    : User's school.        [Optional]
            * college   : User's college.       [Optional]
            * grade     : User's grade.         [Optional]
            * class_num : User's class number.  [Optional]

            * id_name   : User's id-card name.   [Optional]
            * id_number : User's id-card number. [Optional]
            * id_photos : User's id-card photos. [Optional]
        """
        try:
            user_uid = request.session.get('user_uid')

            input_dict = request.POST

            if 'sex' in input_dict:
                sex = input_dict.get('sex')

                assert sex in SexType.__dict__.keys() and \
                    not sex.startswith('__'), 'sex error'

            if 'avatar' in input_dict:
                avatar = input_dict.get('avatar')

                assert avatar.startswith('http://') or\
                    avatar.startswith('https://'),\
                    'avatar is not an available URL'

            if 'id_number' in input_dict:
                id_number = input_dict.get('id_number')

                assert id_number_is_available(id_type = IDType.idcard,\
                                            id_number = id_number),\
                    'id_number verify error'

            data = {}

            u_info_lst = ['sex', 'avatar', 'school', 'college', 'grade', 'class_num']
            u_id_lst   = ['id_name', 'id_number', 'id_photos']

            # UserInfo data update
            u_info = None
            u_info_updated = False

            for key in u_info_lst:
                if key in input_dict:
                    u_info = u_info or UserInfo.objects.get(user = user_uid)

                    setattr(u_info, key, input_dict.get(key))

                    u_info_updated = True

            if u_info_updated:
                u_info.save()

            # UserIdentity data update
            u_id = None
            u_id_updated = False

            for key in u_id_lst:
                if key in input_dict:

                    if key == 'id_photos':
                        id_photos = json.loads(input_dict.get('id_photos'))
                        input_dict['id_photos'] = json.dumps(id_photos)

                    u_id = u_id or UserIdentity.objects.get(user = user_uid)

                    setattr(u_id, key, input_dict.get(key))

                    u_id_updated = True

            if u_id_updated:
                u_id.save()

            if u_id_updated or u_id_updated:
                u_obj = UserCache(user_uid = user_uid)
                u_obj.update_info()

                data = u_obj.get_simple_info()

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)


class UserBankAccountView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-07-02
    Modify : 2016-07-02 by Garvey
    --------------------------------
    Supported methods: POST, PUT
    """
    @method_decorator(require_login)
    def post(self, request, *args, **kwargs):
        """
        Create or update bank account.

        Params : 
            * bank_name      : User's account bank.         [Required]
            * account_name   : User's account name.         [Required]
            * account_number : User's account number.       [Required]
            * card_photos    : User's account card photos.  [Required]
        """
        try:
            user_uid = request.session.get('user_uid')

            bank_name      = request.POST.get('bank_name', None)
            account_name   = request.POST.get('account_name', None)
            account_number = request.POST.get('account_number', None)
            card_photos    = request.POST.get('card_photos', None)

            assert bank_name, 'bank_name is required'
            assert account_name, 'account_name is required'
            assert account_number and account_number.isdigit(),\
                'account_number is required and must be digits'
            assert card_photos, 'card_photos is required'

            card_photos = json.loads(card_photos)
            card_photos = json.dumps(card_photos)

            u_ba, created = UserBankAccount.objects.get_or_create(         \
                                user_id = user_uid, account_number = account_number,\
                                is_deleted = False,                        \
                                defaults = {'bank_name'    : bank_name,    \
                                            'account_name' : account_name, \
                                            'card_photos'  : card_photos}  )

            if not created:
                u_ba.account_name = account_name
                u_ba.card_photos  = card_photos

                u_ba.save()

            u_obj = UserCache(user_uid = user_uid)
            u_obj.update_info()

            return self.encode_json_response(code = 0)

        except Exception as e:
            raise ErrorException(e)

    @method_decorator(require_login)
    def put(self, request, *args, **kwargs):
        """
        Enable bank account.

        Params : 
            * account_number : User's account number.       [Required]
        """
        try:
            user_uid = request.session.get('user_uid')

            account_number = request.PUT.get('account_number', None)

            assert account_number and account_number.isdigit(),\
                'account_number is required and must be digits'

            UserBankAccount.objects.filter(user = user_uid, \
                    account_number = account_number, is_deleted = False).\
                update(enable = True)

            u_obj = UserCache(user_uid = user_uid)
            u_obj.update_info()

            return self.encode_json_response(code = 0)

        except Exception as e:
            raise ErrorException(e)


class UserTreeView(BaseView):
    """
    --------------------------------
    Author : Garvey Ding
    Created: 2016-07-04
    Modify : 2016-07-04 by Garvey
    --------------------------------
    Supported methods: GET
    """
    @method_decorator(require_login)
    def get(self, request, *args, **kwargs):
        """
        Params : None
        """
        try:
            user_uid = request.session.get('user_uid')

            ut_obj = UserTreeObj(user_uid = user_uid)

            data = {
                'parent'   : ut_obj.get_parent_data(),
                'children' : ut_obj.get_children_data(),
            }

            return self.encode_json_response(code = 0, data = data)

        except Exception as e:
            raise ErrorException(e)

