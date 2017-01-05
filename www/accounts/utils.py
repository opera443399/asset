# coding=utf-8
# ----------------------------------
# @ 2017/1/4
# @ PC
# ----------------------------------

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.conf import settings

class TokenManager(object):
    def generate(self, user):
        return 'test_for_user_{0}'.format(user.pk)

    def validate(self, user, token):
        '''
        just a simple test here
        '''
        t_a = self.generate(user)
        t_b = token
        return t_a == t_b


def validate_new_user_by_email(request, user):
    tpl_email_subject = 'accounts/activation_email_subject.html'
    tpl_email_body = 'accounts/activation_email_body.html'

    website_domain = request.META['SERVER_NAME']

    context_subject = {'website_domain': website_domain}
    subject = render_to_string(tpl_email_subject, context_subject)
    email_subject = ''.join(subject.splitlines())

    token_manager = TokenManager()
    context_body = {
        'protocol': 'https' if request.is_secure() else 'http',
        'website_domain': website_domain,
        'uuid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_manager.generate(user),
    }
    email_body = render_to_string(tpl_email_body, context_body)

    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = [user.email]

    msg = EmailMultiAlternatives(email_subject,
                                 email_body,
                                 email_from,
                                 email_to)
    msg.content_subtype = "html"
    msg.send()
