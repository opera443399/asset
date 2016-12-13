# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-12-13
# @ pc
###################################
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(_('Vendor Name'), max_length=20)
    desc = models.CharField(_('Vendor Description'), max_length=100, default='Extra info.')
    def __str__(self):
        return self.name


class DeviceType(models.Model):
    type_of = models.CharField(_('Host Type'), max_length=10)
    cpu = models.CharField(_('Host CPU'), max_length=20)
    memory = models.CharField(_('Host Memory'), max_length=20)
    disk_ssd = models.CharField(_('Host Disk SSD'), max_length=20, default='none')
    disk_sas = models.CharField(_('Host Disk SAS'), max_length=20, default='none')
    disk_sata = models.CharField(_('Host Disk SATA'), max_length=20, default='none')
    nic = models.CharField(_('Host NIC Card'), max_length=20, default='Onboard')
    psu = models.IntegerField(_('Host PSU'), default=1)
    raid_card = models.CharField(_('Device RAID Card'), max_length=20, null=True, blank=True)
    desc = models.CharField(_('Device Description'), max_length=100, default='Extra info.')

    def __str__(self):
        return self.type_of
        

class IDCInfo(models.Model):
    tag = models.CharField(_('IDC Tag'), max_length=10)
    name = models.CharField(_('IDC Fullname'), max_length=20)
    location = models.CharField(_('IDC Location'), max_length=100, default='Extra info.')
    def __str__(self):
        return self.tag


class OSType(models.Model):
    tag = models.CharField(_('OS Tag'), max_length=20)
    desc = models.CharField(_('OS Description'), max_length=20, default='Extra info.')
    def __str__(self):
        return self.tag


class EndUser(models.Model):
    username = models.CharField(_('Username'), max_length=20)
    department = models.CharField(_('Department'), max_length=20)
    def __str__(self):
        return self.username


class Host(models.Model):
    hostname = models.CharField(_('hostname'), max_length=100, unique=True)
    #
    device_sn = models.CharField(_('Device SN'), max_length=40, null=True, blank=True)
    device_vendor = models.ForeignKey(Vendor)
    device_type = models.ForeignKey(DeviceType)
    device_ipmi_ip = models.GenericIPAddressField(_('Device IPMI IP'), null=True, blank=True)
    device_ipmi_user = models.CharField(_('Device IPMI User'), max_length=20, null=True, blank=True)
    device_ipmi_pass = models.CharField(_('Device IPMI Password'), max_length=40, null=True, blank=True)
    device_raid_level = models.CharField(_('Device RAID Level'), max_length=20, null=True, blank=True)
    #
    asset_no = models.CharField(_('Asset No.'), max_length=100, null=True, blank=True)
    asset_date_in = models.DateTimeField(_('Asset Date In'), auto_now_add=True)
    asset_date_out = models.DateTimeField(_('Asset Date Out'), auto_now=True)
    #
    idc_info = models.ForeignKey(IDCInfo)
    idc_rack= models.IntegerField(_('IDC Rack No.'), default=0)
    idc_rack_h= models.IntegerField(_('IDC Rack Height'), default=0)
    #
    os_ip_wan1 = models.GenericIPAddressField(_('OS IP WAN1'), null=True, blank=True)
    os_ip_wan2 = models.GenericIPAddressField(_('OS IP WAN1'), null=True, blank=True)
    os_ip_lan_mgmt = models.GenericIPAddressField(_('OS IP LAN MGMT'))
    os_ip_lan_stor = models.GenericIPAddressField(_('OS IP LAN STOR'), null=True, blank=True)
    os_ip_lan_biz = models.GenericIPAddressField(_('OS IP LAN BIZ'), null=True, blank=True)
    os_type = models.ForeignKey(OSType)
    os_user_root = models.CharField(_('OS root'), max_length=20)
    os_pass_root = models.CharField(_('Password of root'), max_length=40)
    os_user = models.CharField(_('OS User'), max_length=20, null=True, blank=True)
    os_pass = models.CharField(_('Password of User'), max_length=40, null=True, blank=True)
    #
    is_v_host = models.BooleanField(_('Is Virtualization Host?'), default=False)
    is_monited = models.BooleanField(_('Is Monited?'), default=False)
    #
    app_desc = models.CharField(_('App Description'), max_length=40, default='offline')
    end_user = models.ForeignKey(EndUser)
    
    def __str__(self):
        return self.hostname


class Vm(models.Model):
    hostname = models.CharField(_('hostname'), max_length=100, unique=True)
    on_host = models.ForeignKey(Host)
    #
    os_ip_wan = models.GenericIPAddressField(_('OS IP WAN'), null=True, blank=True)
    os_ip_lan = models.GenericIPAddressField(_('OS IP WAN'))
    os_type = models.ForeignKey(OSType)
    os_user_root = models.CharField(_('OS root'), max_length=20)
    os_pass_root = models.CharField(_('Password of root'), max_length=40)
    os_user = models.CharField(_('OS User'), max_length=20, null=True, blank=True)
    os_pass = models.CharField(_('Password of User'), max_length=40, null=True, blank=True)
    #
    is_monited = models.BooleanField(_('Is Monited?'), default=False)
    #
    app_desc = models.CharField(_('App Description'), max_length=40, default='offline')
    end_user = models.ForeignKey(EndUser)
    mount_point = models.CharField(_('Mount Point'), max_length=40, null=True, blank=True)
    desc = models.CharField(_('VM Description'), max_length=100, default='Extra info.')

    def __str__(self):
        return self.hostname
