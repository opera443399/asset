# coding=utf-8
# ----------------------------------
# @ 2016/12/29
# @ PC
# ----------------------------------

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Vendor, DeviceType, InstanceType, IDCInfo, OSType, EndUser, Cluster, Machine, Vm

# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')
    search_fields = ['name']


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'cpu', 'memory', 'disk_ssd', 'disk_sas', 'disk_sata',
                    'nic', 'psu', 'raid_card', 'desc')
    search_fields = ['tag']


class InstanceTypeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'cpu', 'memory', 'desc')
    search_fields = ['tag']


class IDCInfoAdmin(admin.ModelAdmin):
    list_display = ('tag', 'name', 'location', 'desc')
    search_fields = ['tag', 'name']


class OSTypeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'desc')
    search_fields = ['tag']


class EndUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'fullname', 'department')
    search_fields = ['username', 'fullname', 'department']


class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')
    search_fields = ['name']


class MachineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['hostname', 'cluster']}),
        (_('OS'), {'fields': ['os_ip_wan1', 'os_ip_wan2', 'os_ip_lan_mgmt', 'os_ip_lan_stor',
                              'os_ip_lan_biz', 'os_type', 'os_user_root', 'os_pass_root',
                              'os_user_guest', 'os_pass_guest']}),
        (_('APP'), {'fields': ['app_desc', 'operator']}),
        (_('Status'), {'fields': ['is_monited', 'is_online', 'is_v_host']}),
        (_('Device'), {'fields': ['device_sn', 'vendor', 'model', 'device_ipmi_ip','device_ipmi_user',
                                  'device_ipmi_pass', 'device_raid_level', 'desc']}),
        (_('IDC Info'), {'fields': ['idc', 'idc_rack', 'idc_rack_h']}),
        (_('Asset'), {'fields': ['asset_no']}),
        (_('Date information'), {'fields': ['dt_created']}),
    ]
    list_display = ('hostname', 'cluster', 'idc', 'os_ip_wan1', 'os_ip_lan_mgmt', 'os_type',
                    'app_desc', 'operator',
                    'model', 'device_ipmi_ip', 'device_raid_level',
                    'is_monited', 'is_online', 'is_v_host')
    list_filter = ['model', 'device_raid_level', 'idc', 'os_type', 'operator', 'dt_created']
    search_fields = ['hostname', 'device_ipmi_ip', 'os_ip_wan1', 'os_ip_lan_mgmt', 'app_desc']


class VmAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['hostname', 'on_host', 'on_cluster']}),
        (_('OS'), {'fields': ['os_ip_wan', 'os_ip_lan', 'os_type', 'os_user_root', 'os_pass_root',
                              'os_user_guest', 'os_pass_guest']}),
        (_('Status'), {'fields': ['is_monited', 'is_online']}),
        (_('APP'), {'fields': ['app_desc', 'operator', 'mount_point', 'desc']}),
        (_('Date information'), {'fields': ['dt_created']}),
    ]
    list_display = ('hostname', 'on_host', 'on_cluster', 'os_ip_wan', 'os_ip_lan', 'os_type',
                    'app_desc', 'operator', 'instance_type',
                    'is_monited', 'is_online', 'was_added_recently')
    list_filter = ['on_host', 'on_cluster', 'os_type', 'operator', 'instance_type', 'dt_created']
    search_fields = ['hostname', 'os_ip_wan', 'os_ip_lan', 'app_desc']


admin.site.register(Vendor, VendorAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(InstanceType, InstanceTypeAdmin)
admin.site.register(IDCInfo, IDCInfoAdmin)
admin.site.register(OSType, OSTypeAdmin)
admin.site.register(EndUser, EndUserAdmin)
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Vm, VmAdmin)
