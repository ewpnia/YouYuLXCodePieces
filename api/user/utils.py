import hashlib
import hmac
import re
import random
import string
import urllib
import urllib2
import uuid

from django.conf import settings

from common.utils import get_cache, set_cache, delete_cache, generate_random_string

from user.models import User, UserInfo, UserIdentity


def generate_db_pw(org_pw, mobile_phone):
    account_prefix = settings.ACCOUNT_PREFIX

    pf_pw = ''.join((org_pw, account_prefix, mobile_phone))
    hash_pw = hashlib.md5(pf_pw).hexdigest()

    return hash_pw


def mobile_phone_is_available(mobile_phone):
    pattern = settings.MOBILE_PHONE_PATTERN
    result  = re.match(pattern, mobile_phone)

    # If mobile phone number is available, pattern will be matched,
    # so result is not None.

    return False if result is None else True


def id_number_is_available(id_type, id_number):
    if id_type == 'idcard':
        pattern = settings.ID_CARD_PATTERN

    elif id_type == 'passport':
        pattern = settings.PASSPORT_PATTERN

    elif id_type == 'hk_macau_eep':
        pattern = settings.HK_MACAU_EEP_PATTERN

    elif id_type == 'student_card':
        pattern = settings.STUDENT_CARD_PATTERN

    else:
        pattern = settings.ALLWAYS_NONE_PATTERN

    # If id_number is available, pattern will be matched,
    # so result is not None.
    result  = re.match(pattern, id_number)

    return False if result is None else True


def generate_unique_code():

    # seed_1 = random.sample(list(string.letters), 4)
    # seed_2 = str(time.time()).replace('.','')
    # seed_fin = seed_1 + seed_2
    # random.shuffle(seed_fin)
    # code = ''.join(seed_fin)

    # token = hmac.new(uuid.uuid1().bytes, digestmod=hashlib.sha1)
    # Default digestmod is hashlib.md5

    token = hmac.new(uuid.uuid1().bytes)
    return token.hexdigest()


def generate_share_token():
     
    share_token = generate_random_string(length = settings.USER_SHARE_TOKEN_LENGTH)

    while User.objects.filter(share_token = share_token).exists():
        share_token = generate_random_string(length = settings.USER_SHARE_TOKEN_LENGTH)

    return share_token


def generate_join_token():
     
    join_token = generate_random_string(length = settings.USER_JOIN_TOKEN_LENGTH)

    while User.objects.filter(join_token = join_token).exists():
        join_token = generate_random_string(length = settings.USER_JOIN_TOKEN_LENGTH)

    return join_token


