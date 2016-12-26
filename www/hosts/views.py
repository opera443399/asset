#!/bin/env python
# coding=utf-8
# ----------------------------------
# @ 2016/12/26
# @ PC
# ----------------------------------

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

# Create your views here.


def show_index(request):
    """test only"""
    msgs = _('a quick way to build a simple idc resource management page via django, do not use excel.')
    context = msgs
    return HttpResponse(context)
