#!/bin/env python
# coding=utf-8
# ----------------------------------
# @ 2016/12/26
# @ PC
# ----------------------------------

from django.conf.urls import url
from . import views

app_name = 'hosts'
urlpatterns = [
    #################################### /hosts/xxx
    #
    url(r'^$', views.show_index, name='show_index'),
]
