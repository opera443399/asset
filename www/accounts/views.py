# coding=utf-8
# ----------------------------------
# @ 2017/1/4
# @ PC
# ----------------------------------

from django.contrib.auth import login, get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, resolve_url
from django.utils.translation import ugettext as _
from django.utils.http import urlsafe_base64_decode

from .apps import AccountsConfig as conf
from .forms import RegistrationForm
from .utils import TokenManager, validate_new_user_by_email

# Create your views here.


def registration(request, registration_form=RegistrationForm):
    registered_user_redirect_to = conf.LOGIN_REDIRECT_URL
    post_registration_redirect = reverse('accounts:registration_finished')

    if request.user.is_authenticated():
        return redirect(registered_user_redirect_to)

    if not conf.REGISTRATION_IS_OPEN:
        return redirect(reverse('accounts:registration_closed'))

    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            if conf.IS_AUTOACTIVE:
                if conf.REGISTRATION_IS_AUTOLOGIN:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
            elif conf.IS_NEW_USER_NEED_VERIFY_BY_EMAIL:
                try:
                    validate_new_user_by_email(request, user)
                except Exception as e:
                    print('[ERROR] failed to execute "validate_new_user_by_email"\n'
                          ' Reason:\n{0}'.format(e))
            return redirect(post_registration_redirect)
    else:
        form = registration_form()

    context = {
        'thisform': form,
    }

    return render(request, 'accounts/registration.html', context)


def registration_closed(request):
    return render(request, 'accounts/registration_closed.html')


def registration_finished(request):
    return render(request, 'accounts/registration_finished.html')


def activation(request, uuid, token):
    user_model = get_user_model()
    token_manager = TokenManager()
    new_user_is_actived = False

    try:
        uid = urlsafe_base64_decode(uuid)
        user = user_model._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None
    if user and token_manager.validate(user, token):
        user.is_active = True
        user.save()
        new_user_is_actived = True

    context = {
            'new_user_is_actived': new_user_is_actived
            }
    return render(request, 'accounts/activation.html', context)


def profile(request):
    return render(request, 'accounts/profile.html')
