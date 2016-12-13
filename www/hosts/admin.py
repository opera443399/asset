# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-12-13
# @ pc
###################################

from django.contrib import admin

from .models import Vendor, DeviceType, IDCInfo, OSType, EndUser, Host, Vm

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    search_fields = ['name']

class DeviceTypeAdmin(admin.ModelAdmin):
    search_fields = ['type_of']

class IDCInfoAdmin(admin.ModelAdmin):
    search_fields = ['tag']

class OSTypeAdmin(admin.ModelAdmin):
    search_fields = ['tag']

class EndUserAdmin(admin.ModelAdmin):
    search_fields = ['username']

class HostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['hostname']}),
        ('Device', {'fields': ['device_sn', 'device_vendor', 'device_type', 'device_ipmi_ip', 'device_ipmi_user', 'device_ipmi_pass', 'device_raid_level']}),
        ('IDC Info', {'fields':['idc_info', 'idc_rack', 'idc_rack_h']}),
        ('OS', {'fields':['os_ip_wan1', 'os_ip_wan2', 'os_ip_lan_mgmt', 'os_ip_lan_stor', 'os_ip_lan_biz', 'os_type', 'os_user_root', 'os_pass_root', 'os_user', 'os_pass']}),
        ('Status', {'fields':['is_monited', 'is_online', 'is_v_host']}),
        ('APP', {'fields':['app_desc', 'end_user']}),
        ('Asset', {'fields':['asset_no']}),
        ('Date information', {'fields': ['dt_created', 'dt_destroyed'], 'classes': ['collapse']}),
    ]
    list_display = ('hostname', 'idc_info', 'os_ip_wan1', 'os_ip_lan_mgmt', 'os_type', 'app_desc', 'end_user',
                    'device_type', 'device_ipmi_ip', 'device_raid_level',
                    'is_monited', 'is_online', 'is_v_host', 'was_added_recently')
    list_filter = ['device_type', 'device_raid_level', 'idc_info', 'os_type', 'end_user', 'dt_created']
    search_fields = ['hostname', 'device_ipmi_ip', 'os_ip_wan1', 'os_ip_lan_mgmt', 'app_desc']


class VmAdmin(admin.ModelAdmin):
    search_fields = ['hostname']
    fieldsets = [
        (None, {'fields': ['hostname','on_host']}),
        ('OS', {'fields': ['os_ip_wan', 'os_ip_lan', 'os_type', 'os_user_root', 'os_pass_root', 'os_user', 'os_pass']}),
        ('Status', {'fields':['is_monited', 'is_online']}),
        ('APP', {'fields':['app_desc', 'end_user', 'mount_point', 'desc']}),
        ('Date information', {'fields': ['dt_created', 'dt_destroyed'], 'classes': ['collapse']}),
    ]
    list_display = ('hostname', 'on_host', 'os_ip_wan', 'os_ip_lan', 'os_type', 'app_desc', 'end_user',
                    'is_monited', 'is_online', 'was_added_recently')    
    list_filter = ['on_host', 'os_type', 'end_user', 'dt_created']
    search_fields = ['hostname', 'os_ip_wan', 'os_ip_lan', 'app_desc']


admin.site.register(Vendor, VendorAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(IDCInfo, IDCInfoAdmin)
admin.site.register(OSType, OSTypeAdmin)
admin.site.register(EndUser, EndUserAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Vm, VmAdmin)

