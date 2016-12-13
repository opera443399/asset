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
    search_fields = ['hostname']

class VmAdmin(admin.ModelAdmin):
    search_fields = ['hostname']


admin.site.register(Vendor, VendorAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(IDCInfo, IDCInfoAdmin)
admin.site.register(OSType, OSTypeAdmin)
admin.site.register(EndUser, EndUserAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Vm, VmAdmin)

