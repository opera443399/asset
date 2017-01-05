# coding=utf-8
# ----------------------------------
# @ 2017/1/4
# @ PC
# ----------------------------------

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'
urlpatterns = [
    #################################### accounts
    #
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    #
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^registration/closed/$', views.registration_closed, name='registration_closed'),
    url(r'^registration/finished/$', views.registration_finished, name='registration_finished'),

    #
    url(r'^activation/(?P<uuid>[0-9a-zA-Z_\-]+)/(?P<token>[0-9a-zA-Z_]+)/$', views.activation, name='activation'),

    #
    url(r'^profile/$', views.profile, name='profile'),
]
