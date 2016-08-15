from django.conf import settings

def get_code_msg(code, default_msg = ''):
    code = int(code)
    return settings.CODE_MSG.get(code, default_msg)
    