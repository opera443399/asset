# coding=utf-8
# ----------------------------------
# @ 2016/12/27
# @ PC
# ----------------------------------

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import os
from .models import OSType, EndUser, Machine, Vm
# Create your views here.


def show_index(request):
    """test only"""
    msgs = _('a quick way to build a simple idc resource management page via django, do not use excel.')
    context = msgs
    return HttpResponse(context)


def load_data_vms(request):
    """ exp: how to import a list of vms to db
        tips: you have to prepare something before this step:
        1. hosts has been added.
        2. os_type has been added.
        3. operator has been added.
    """
    vm_status = {}
    f_data = "{0}{1}{2}".format(os.getcwd(), os.sep, 'vms.csv')
    with open(f_data) as f:
        for line in f:
            if line.startswith('#'):
                continue
            # parse csv fields
            try:
                hostname, on_host, os_ip_lan, os_pass_root, os_pass_guest, \
                    app_desc, os_type, operator = line.strip('\n').split(',')

                # objects for ForeignKey
                obj_host = Machine.objects.get(hostname=on_host)
                obj_os_type = OSType.objects.get(tag=os_type)
                obj_operator = EndUser.objects.get(username=operator)
                dt_now = timezone.now()

                # import data to db
                Vm.objects.get_or_create(hostname=hostname,
                              on_host=obj_host,
                              os_ip_lan=os_ip_lan,
                              os_pass_root=os_pass_root,
                              os_pass_guest=os_pass_guest,
                              is_monited=True,
                              is_online=True,
                              app_desc=app_desc,
                              os_type=obj_os_type,
                              operator=obj_operator,
                              dt_created=dt_now
                              )
            except Exception as e:
                context = 'error: {0}'.format(e)
                vm_status[hostname] = context
                continue

            vm_status[hostname] = 'ok.'

    msgs = ''
    for k,v in sorted(vm_status.items()):
        msgs += '{0} -> <font color="red">{1}</font><br/>'.format(k, v)
    context = '[*] parsed: <br/>{0}'.format(msgs)
    return HttpResponse(context)