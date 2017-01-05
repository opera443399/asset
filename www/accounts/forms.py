# coding=utf-8
# ----------------------------------
# @ 2017/1/4
# @ PC
# ----------------------------------

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .apps import AccountsConfig as conf
from .fields import PasswordField, UserEmailField

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email',)
        #fields = '__all__'

    error_messages = {
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    email = UserEmailField(label=_('Email Address'), max_length=255)
    password1 = PasswordField(label=_('Password'))
    password2 = PasswordField(
        label=_('Password Confirmation'),
        help_text=_('Enter the same password as above, for verification.'))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = conf.IS_AUTOACTIVE
        if commit:
            user.save()
        return user

class RegistrationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'
