# coding=utf-8
# ----------------------------------
# @ 2017/1/4
# @ PC
# ----------------------------------

from __future__ import unicode_literals

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    LOGIN_REDIRECT_URL = '/'

    PASSWORD_LEN_MIN = 5
    PASSWORD_LEN_MAX = None
    PASSWORD_COMPLEXITY_CHECK = True
    PASSWORD_POLICY = {
        'UPPER': 1,       # Uppercase 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        'LOWER': 1,       # Lowercase 'abcdefghijklmnopqrstuvwxyz'
        'DIGITS': 1,      # Digits '0123456789'
        'PUNCTUATION': 0  # Punctuation """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    }

    EMAIL_DOMAIN_VALIDATE = True
    EMAIL_DOMAINS_BLACKLIST = []
    EMAIL_DOMAINS_WHITELIST = []

    REGISTRATION_IS_OPEN = True
    IS_AUTOACTIVE = False
    REGISTRATION_IS_AUTOLOGIN = True
    IS_NEW_USER_NEED_VERIFY_BY_EMAIL = False


