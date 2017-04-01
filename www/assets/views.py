# coding=utf-8
# ----------------------------------
# @ 2017/4/1
# @ PC
# ----------------------------------

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os
from .models import Vendor, DeviceType, InstanceType, IDCInfo, OSType, \
    EndUser, Cluster, BusinessUnit, RuntimeEnvironment, Machine, Vm

from rest_framework import viewsets, permissions
from .serializers import VendorSerializer, DeviceTypeSerializer, InstanceTypeSerializer, IDCInfoSerializer, \
    OSTypeSerializer, EndUserSerializer, ClusterSerializer, BusinessUnitSerializer, RuntimeEnvironmentSerializer


# Create your views here.
# ================================ API ================================
class VendorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DeviceTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class InstanceTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = InstanceType.objects.all()
    serializer_class = InstanceTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IDCInfoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = IDCInfo.objects.all()
    serializer_class = IDCInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)


class OSTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = OSType.objects.all()
    serializer_class = OSTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class EndUserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = EndUser.objects.all()
    serializer_class = EndUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ClusterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BusinessUnitViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RuntimeEnvironmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = RuntimeEnvironment.objects.all()
    serializer_class = RuntimeEnvironmentSerializer
    permission_classes = (permissions.IsAuthenticated,)


# ================================ TEST ================================
def show_index(request):
    """
    index
    """
    return render(request, 'assets/index.html')


def show_about(request):
    """
    about
    """
    return render(request, 'assets/about.html')


# ================================ LIST ================================
@login_required
def list_hosts(request):
    """
    list hosts
    """
    biz_unit_id = 0
    run_env_id = 0
    q = ''
    default_data = Machine.objects.order_by('-run_env')

    if request.method == 'GET':
        ## get filters
        try:
            biz_unit_id = int(request.GET.get('biz_unit'))
        except (KeyError, ValueError, TypeError):
            biz_unit_id = 0

        try:
            run_env_id = int(request.GET.get('run_env'))
        except (KeyError, ValueError, TypeError):
            run_env_id = 0

        try:
            q = request.GET.get('q')
            default_data = default_data.filter(hostname__contains=q)
        except (KeyError, ValueError):
            q = ''

    ## filtering
    if biz_unit_id == 0 and run_env_id == 0:
        data = default_data
    elif biz_unit_id != 0 and run_env_id == 0:
        data = default_data.filter(biz_unit=biz_unit_id).order_by('-run_env')
    elif biz_unit_id == 0 and run_env_id != 0:
        data = default_data.filter(run_env=run_env_id).order_by('-run_env')
    else:
        data = default_data.filter(biz_unit=biz_unit_id).filter(run_env=run_env_id).order_by('-run_env')

    ## pagenation: show 10 rows per page
    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    try:
        list_of_hosts = paginator.page(page)
    except PageNotAnInteger:
        list_of_hosts = paginator.page(1)
    except EmptyPage:
        list_of_hosts = paginator.page(paginator.num_pages)

    biz_units = BusinessUnit.objects.all()
    run_envs = RuntimeEnvironment.objects.all()
    context = {
        'list_of_hosts': list_of_hosts,
        'biz_units': biz_units,
        'run_envs': run_envs,
        'selected_biz_unit_id': biz_unit_id,
        'selected_run_env_id': run_env_id,
        'q': q
    }

    return render(request, 'assets/list_hosts.html', context)


@login_required
def list_vms(request):
    """
    list vms
    """
    biz_unit_id = 0
    run_env_id = 0
    q = ''
    default_data = Vm.objects.order_by('-run_env')

    if request.method == 'GET':
        ## get filters
        try:
            biz_unit_id = int(request.GET.get('biz_unit'))
        except (KeyError, ValueError, TypeError):
            biz_unit_id = 0

        try:
            run_env_id = int(request.GET.get('run_env'))
        except (KeyError, ValueError, TypeError):
            run_env_id = 0

        try:
            q = request.GET.get('q')
            default_data = default_data.filter(hostname__contains=q)
        except (KeyError, ValueError):
            q = ''

    ## filtering
    if biz_unit_id == 0 and run_env_id == 0:
        data = default_data.order_by('-run_env')
    elif biz_unit_id != 0 and run_env_id == 0:
        data = default_data.filter(biz_unit=biz_unit_id).order_by('-run_env')
    elif biz_unit_id == 0 and run_env_id != 0:
        data = default_data.filter(run_env=run_env_id).order_by('-run_env')
    else:
        data = default_data.filter(biz_unit=biz_unit_id).filter(run_env=run_env_id).order_by('-run_env')

    ## pagenation: show 10 rows per page
    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    try:
        list_of_vms = paginator.page(page)
    except PageNotAnInteger:
        list_of_vms = paginator.page(1)
    except EmptyPage:
        list_of_vms = paginator.page(paginator.num_pages)

    biz_units = BusinessUnit.objects.all()
    run_envs = RuntimeEnvironment.objects.all()
    context = {
        'list_of_vms': list_of_vms,
        'biz_units': biz_units,
        'run_envs': run_envs,
        'selected_biz_unit_id': biz_unit_id,
        'selected_run_env_id': run_env_id,
        'q': q
    }

    return render(request, 'assets/list_vms.html', context)


# ================================ IMPORT ================================
@login_required
def import_hosts(request):
    """
    exp: how to import a list of hosts to db
    tips: you have to prepare something before this step:
            cluster, model, os_type, operator, idc
    """
    host_status = {}
    import_count_ok = import_count_fail = 0
    ##cwd()/data/import/*.csv
    f_data = "{0}{1}data{1}import{1}{2}".format(os.getcwd(), os.sep, 'hosts.csv')
    with open(f_data) as f:
        for line in f:
            if line.startswith('#'):
                continue
            # parse csv fields
            hostname = 'Empty Line'
            try:
                hostname, cluster, os_ip_wan1, os_ip_lan_mgmt, os_pass_root, os_pass_guest, app_desc, biz_unit, \
                run_env, os_type, device_sn, model, device_ipmi_ip, device_ipmi_pass, device_raid_level, idc, \
                idc_rack, idc_rack_h, asset_no, operator = line.strip('\n').split(',')

                # objects for ForeignKey
                obj_cluster = Cluster.objects.get(name=cluster)
                obj_model = DeviceType.objects.get(tag=model)
                obj_os_type = OSType.objects.get(tag=os_type)
                obj_operator = EndUser.objects.get(username=operator)
                obj_idc = IDCInfo.objects.get(tag=idc)
                obj_biz_unit = BusinessUnit.objects.get(name=biz_unit)
                obj_run_env = RuntimeEnvironment.objects.get(name=run_env)
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
                                              biz_unit=obj_biz_unit,
                                              run_env=obj_run_env,
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
                import_count_ok += 1
            except Exception as e:
                context = 'error: {0}'.format(e)
                host_status[hostname] = context
                import_count_fail += 1
                continue

    msgs = ''
    for k, v in sorted(host_status.items()):
        msgs += '<br/>{0} -> <font color="red">{1}</font>'.format(k, v)
    if not msgs:
        msgs = 'no data!'
    else:
        msgs += '<br/><br/>success: {0}, failure: <font color="red">{1}</font>.'.format(
                import_count_ok, import_count_fail)
    context = {'msgs': '[*] import result: {0}'.format(msgs)}

    return render(request, 'assets/import.html', context)


@login_required
def import_vms(request):
    """
    exp: how to import a list of vms to db
    tips: you have to prepare something before this step:
            host, os_type, operator
    """
    import_status = {}
    import_count_ok = import_count_fail = 0
    ##cwd()/data/import/*.csv
    f_data = "{0}{1}data{1}import{1}{2}".format(os.getcwd(), os.sep, 'vms.csv')
    with open(f_data) as f:
        for line in f:
            if line.startswith('#'):
                continue
            # parse csv fields
            hostname = 'Empty Line'
            try:
                hostname, on_host, on_cluster, os_ip_wan, os_ip_lan, os_pass_root, os_pass_guest, \
                app_desc, biz_unit, run_env, os_type, operator = line.strip('\n').split(',')

                # objects for ForeignKey
                obj_host = Machine.objects.get(hostname=on_host)
                obj_cluster = Cluster.objects.get(name=on_cluster)
                obj_os_type = OSType.objects.get(tag=os_type)
                obj_operator = EndUser.objects.get(username=operator)
                obj_biz_unit = BusinessUnit.objects.get(name=biz_unit)
                obj_run_env = RuntimeEnvironment.objects.get(name=run_env)
                dt_now = timezone.now()

                # import data to db
                Vm.objects.get_or_create(hostname=hostname,
                                         on_host=obj_host,
                                         on_cluster=obj_cluster,
                                         os_ip_wan=os_ip_wan,
                                         os_ip_lan=os_ip_lan,
                                         os_pass_root=os_pass_root,
                                         os_pass_guest=os_pass_guest,
                                         is_monited=True,
                                         is_online=True,
                                         app_desc=app_desc,
                                         biz_unit=obj_biz_unit,
                                         run_env=obj_run_env,
                                         os_type=obj_os_type,
                                         operator=obj_operator,
                                         dt_created=dt_now
                                         )
                import_status[hostname] = 'ok.'
                import_count_ok += 1
            except Exception as e:
                context = 'error: {0}'.format(e)
                import_status[hostname] = context
                import_count_fail += 1
                continue

    msgs = ''
    for k, v in sorted(import_status.items()):
        msgs += '<br/>{0} -> <font color="red">{1}</font>'.format(k, v)
    if not msgs:
        msgs = 'no data!'
    else:
        msgs += '<br/><br/>success: {0}, failure: <font color="red">{1}</font>.'.format(
                import_count_ok, import_count_fail)
    context = {'msgs': '[*] import result: {0}'.format(msgs)}

    return render(request, 'assets/import.html', context)
