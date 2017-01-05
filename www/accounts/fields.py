# coding=utf-8
# ----------------------------------
# @ 2017/1/4
# @ PC
# ----------------------------------

from django import forms
from django.core.validators import validate_email
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

import string
from .apps import AccountsConfig as conf

class ValidateLength(object):
    code = 'length'

    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length or conf.PASSWORD_LEN_MIN
        self.max_length = max_length or conf.PASSWORD_LEN_MAX

    def __call__(self, value):
        if self.min_length and len(value) < self.min_length:
            raise forms.ValidationError(
                _('Password too short (must be %s characters or more)') % self.min_length,
                code=self.code)
        elif self.max_length and len(value) > self.max_length:
            raise forms.ValidationError(
                _('Password too long (must be %s characters or less)') % self.max_length,
                code=self.code)


class ValidateComplexity(object):
    code = 'complexity'
    message = _('Weak password, %s')

    def __init__(self):
        self.password_policy = conf.PASSWORD_POLICY

    def __call__(self, value):
        if not conf.PASSWORD_COMPLEXITY_CHECK:
            return

        uppercase, lowercase, digits, non_ascii, punctuation = set(), set(), set(), set(), set()

        for char in value:
            if char.isupper():
                uppercase.add(char)
            elif char.islower():
                lowercase.add(char)
            elif char.isdigit():
                digits.add(char)
            elif char in string.punctuation:
                punctuation.add(char)
            else:
                non_ascii.add(char)

        if len(uppercase) < self.password_policy.get('UPPER', 0):
            raise forms.ValidationError(
                self.message % _('must contain %(UPPER)s or '
                                 'more uppercase characters (A-Z)') % self.password_policy,
                code=self.code)
        elif len(lowercase) < self.password_policy.get('LOWER', 0):
            raise forms.ValidationError(
                self.message % _('Must contain %(LOWER)s or '
                                 'more lowercase characters (a-z)') % self.password_policy,
                code=self.code)
        elif len(digits) < self.password_policy.get('DIGITS', 0):
            raise forms.ValidationError(
                self.message % _('must contain %(DIGITS)s or '
                                 'more numbers (0-9)') % self.password_policy,
                code=self.code)
        elif len(punctuation) < self.password_policy.get('PUNCTUATION', 0):
            raise forms.ValidationError(
                self.message % _('must contain %(PUNCTUATION)s or more '
                                 'symbols') % self.password_policy,
                code=self.code)


class ValidateEmailFormat(object):
    message = _('Sorry, %s emails are not allowed. Please use a different email address.')
    code = 'invalid'

    def __init__(self, ):
        self.domain_blacklist = conf.EMAIL_DOMAINS_BLACKLIST
        self.domain_whitelist = conf.EMAIL_DOMAINS_WHITELIST

    def __call__(self, value):
        if not conf.EMAIL_DOMAIN_VALIDATE:
            return

        if not value or '@' not in value:
            raise forms.ValidationError(_('Enter a valid email address.'), code=self.code)

        value = force_text(value)
        user_part, domain_part = value.rsplit('@', 1)

        if self.domain_blacklist and domain_part in self.domain_blacklist:
            raise forms.ValidationError(self.message % domain_part, code=self.code)

        if self.domain_whitelist and domain_part not in self.domain_whitelist:
            raise forms.ValidationError(self.message % domain_part, code=self.code)


validate_length = ValidateLength()
validate_complexity = ValidateComplexity()
validate_email_format = ValidateEmailFormat()


class PasswordField(forms.CharField):
    widget = forms.PasswordInput()
    default_validators = [validate_length, validate_complexity]


class UserEmailField(forms.EmailField):
    default_validators = [validate_email, validate_email_format]


