# coding=utf-8
# ----------------------------------
# @ 2016/12/27
# @ PC
# ----------------------------------

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import os
from .models import DeviceType, IDCInfo, OSType, EndUser, Cluster, Machine, Vm
# Create your views here.


def show_index(request):
    """test only"""
    msgs = _('a quick way to build a simple idc resource management page via django, do not use excel.')
    context = msgs
    return HttpResponse(context)


def load_data_hosts(request):
    """ exp: how to import a list of hosts to db
        tips: you have to prepare something before this step:
            cluster, model, os_type, operator, idc
    """
    host_status = {}
    f_data = "{0}{1}{2}".format(os.getcwd(), os.sep, 'hosts.csv')
    with open(f_data) as f:
        for line in f:
            if line.startswith('#'):
                continue
            # parse csv fields
            try:
                hostname = 'Empty Line'
                hostname, cluster, os_ip_wan1, os_ip_lan_mgmt, os_pass_root, os_pass_guest, app_desc, os_type, \
                    device_sn, model, device_ipmi_ip, device_ipmi_pass, device_raid_level, idc, idc_rack, \
                    idc_rack_h, asset_no, operator = line.strip('\n').split(',')

                # objects for ForeignKey
                obj_cluster = Cluster.objects.get(name=cluster)
                obj_model = DeviceType.objects.get(tag=model)
                obj_os_type = OSType.objects.get(tag=os_type)
                obj_operator = EndUser.objects.get(username=operator)
                obj_idc = IDCInfo.objects.get(tag=idc)
                dt_now = timezone.now()

                # import data to db
                Machine.objects.get_or_create(hostname=hostname,
                                         cluster=obj_cluster,
                                         os_ip_wan1=os_ip_wan1,
                                         os_ip_lan_mgmt=os_ip_lan_mgmt,
                                         os_type=obj_os_type,
                                         os_pass_root=os_pass_root,
                                         os_pass_guest=os_pass_guest,
                                         app_desc=app_desc,
                                         operator=obj_operator,
                                         is_monited=True,
                                         is_online=True,
                                         is_v_host=True,
                                         device_sn=device_sn,
                                         model=obj_model,
                                         device_ipmi_ip=device_ipmi_ip,
                                         device_ipmi_pass=device_ipmi_pass,
                                         device_raid_level=device_raid_level,
                                         idc=obj_idc,
                                         idc_rack=idc_rack,
                                         idc_rack_h=idc_rack_h,
                                         asset_no=asset_no,
                                         dt_created=dt_now
                                         )
                host_status[hostname] = 'ok.'
            except Exception as e:
                context = 'error: {0}'.format(e)
                host_status[hostname] = context
                continue


    msgs = ''
    for k,v in sorted(host_status.items()):
        msgs += '<br/>{0} -> <font color="red">{1}</font>'.format(k, v)
    if not msgs:
        msgs = 'no data!'
    context = '[*] result for vms: {0}'.format(msgs)
    return HttpResponse(context)


def load_data_vms(request):
    """ exp: how to import a list of vms to db
        tips: you have to prepare something before this step:
            host, os_type, operator
    """
    vm_status = {}
    f_data = "{0}{1}{2}".format(os.getcwd(), os.sep, 'vms.csv')
    with open(f_data) as f:
        for line in f:
            if not line:
                continue
            if line.startswith('#'):
                continue
            # parse csv fields
            try:
                hostname = 'Empty Line'
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
                vm_status[hostname] = 'ok.'
            except Exception as e:
                context = 'error: {0}'.format(e)
                vm_status[hostname] = context
                continue



    msgs = ''
    for k,v in sorted(vm_status.items()):
        msgs += '<br/>{0} -> <font color="red">{1}</font>'.format(k, v)
    if not msgs:
        msgs = 'no data!'
    context = '[*] result for vms: {0}'.format(msgs)
    return HttpResponse(context)