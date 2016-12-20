# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-12-20
# @ pc
###################################

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import datetime

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(_('Vendor Name'), max_length=20)
    desc = models.CharField(_('Vendor Description'), max_length=100, default='Extra info.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Vendors')
        verbose_name_plural = _('Vendors')


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

    class Meta:
        verbose_name = _('Device Type')
        verbose_name_plural = _('Device Type')


class IDCInfo(models.Model):
    tag = models.CharField(_('IDC Tag'), max_length=10)
    name = models.CharField(_('IDC Fullname'), max_length=20)
    location = models.CharField(_('IDC Location'), max_length=100, default='Extra info.')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = _('IDC')
        verbose_name_plural = _('IDC')


class OSType(models.Model):
    tag = models.CharField(_('OS Tag'), max_length=20)
    desc = models.CharField(_('OS Description'), max_length=20, default='Extra info.')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = _('OS Type')
        verbose_name_plural = _('OS Type')


class Client(models.Model):
    username = models.CharField(_('Username'), max_length=20)
    department = models.CharField(_('Department'), max_length=20)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Client')


class Cluster(models.Model):
    name = models.CharField(_('Cluster Name'), max_length=20)
    desc = models.CharField(_('Cluster Description'), max_length=20, default='Extra info.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Cluster')
        verbose_name_plural = _('Cluster')


class Machine(models.Model):
    hostname = models.CharField(_('hostname'), max_length=100, unique=True)
    cluster = models.ForeignKey(Cluster, default='1', verbose_name=_('Cluster'))
    #
    os_ip_wan1 = models.GenericIPAddressField(_('IP_WAN1'), null=True, blank=True)
    os_ip_wan2 = models.GenericIPAddressField(_('IP_WAN2'), null=True, blank=True)
    os_ip_lan_mgmt = models.GenericIPAddressField(_('IP_LAN_MGMT'))
    os_ip_lan_stor = models.GenericIPAddressField(_('IP_LAN_STOR'), null=True, blank=True)
    os_ip_lan_biz = models.GenericIPAddressField(_('IP_LAN_BIZ'), null=True, blank=True)
    os_type = models.ForeignKey(OSType, default='1', verbose_name=_('OS Type'))
    os_user_root = models.CharField(_('Admin'), max_length=20)
    os_pass_root = models.CharField(_('Password of Admin'), max_length=40)
    os_user_guest = models.CharField(_('Guest'), max_length=20, null=True, blank=True)
    os_pass_guest = models.CharField(_('Password of Guest'), max_length=40, null=True, blank=True)
    #
    app_desc = models.CharField(_('App Description'), max_length=40, default='NOT_IN_USE')
    client = models.ForeignKey(Client, default='1', verbose_name=_('Client'))
    #
    is_monited = models.BooleanField(_('Is Monited?'), default=False)
    is_online = models.BooleanField(_('Is Online?'), default=False)
    is_v_host = models.BooleanField(_('Is Virt Host?'), default=False)
    #
    device_sn = models.CharField(_('SN'), max_length=40, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, default='1', verbose_name=_('Vendor'))
    model = models.ForeignKey(DeviceType, default='1', verbose_name=_('Model'))
    device_ipmi_ip = models.GenericIPAddressField(_('IPMI IP'), null=True, blank=True)
    device_ipmi_user = models.CharField(_('IPMI User'), max_length=20, null=True, blank=True)
    device_ipmi_pass = models.CharField(_('IPMI Password'), max_length=40, null=True, blank=True)
    device_raid_level = models.CharField(_('RAID'), max_length=20, null=True, blank=True)
    #
    idc = models.ForeignKey(IDCInfo, default='1', verbose_name=_('IDC'))
    idc_rack = models.CharField(_('IDC Rack No.'), max_length=10, default='0')
    idc_rack_h = models.IntegerField(_('IDC Rack Height'), default=0)
    #
    asset_no = models.CharField(_('Asset No.'), max_length=100, null=True, blank=True)
    dt_created = models.DateTimeField(_('When Created?'))
    dt_destroyed = models.DateTimeField(_('When Destroyed?'), null=True, blank=True)
    
    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = _('Machines')
        verbose_name_plural = _('Machines')

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.dt_created <= now

    was_added_recently.admin_order_field = 'dt_created'
    was_added_recently.boolean = True
    was_added_recently.short_description = _('Added recently?')


class Vm(models.Model):
    hostname = models.CharField(_('hostname'), max_length=100, unique=True)
    on_host = models.ForeignKey(Machine, default='1', verbose_name=_('On Host'))
    on_cluster = models.ForeignKey(Cluster, default='1', verbose_name=_('On Cluster'))
    #
    os_ip_wan = models.GenericIPAddressField(_('IP_WAN'), null=True, blank=True)
    os_ip_lan = models.GenericIPAddressField(_('IP_LAN'))
    os_type = models.ForeignKey(OSType, default='1', verbose_name=_('OS Type'))
    os_user_root = models.CharField(_('Admin'), max_length=20)
    os_pass_root = models.CharField(_('Password of Admin'), max_length=40)
    os_user_guest = models.CharField(_('Guest'), max_length=20, null=True, blank=True)
    os_pass_guest = models.CharField(_('Password of Guest'), max_length=40, null=True, blank=True)
    #
    is_monited = models.BooleanField(_('Is Monited?'), default=False)
    is_online = models.BooleanField(_('Is Online?'), default=False)
    #
    app_desc = models.CharField(_('App Description'), max_length=40, default='NOT_IN_USE')
    client = models.ForeignKey(Client, default='1', verbose_name=_('Client'))
    mount_point = models.CharField(_('Mount Point'), max_length=40, null=True, blank=True)
    desc = models.CharField(_('VM Description'), max_length=100, default='Extra info.')
    #
    dt_created = models.DateTimeField(_('When Created?'))
    dt_destroyed = models.DateTimeField(_('When Destroyed?'), null=True, blank=True)

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = _('VMs')
        verbose_name_plural = _('VMs')

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.dt_created <= now
    was_added_recently.admin_order_field = 'dt_created'
    was_added_recently.boolean = True
    was_added_recently.short_description = _('Added recently?')
