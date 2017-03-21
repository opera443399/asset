# coding=utf-8
# ----------------------------------
# @ 2017/3/21
# @ PC
# ----------------------------------


from rest_framework import serializers
from .models import Vendor, DeviceType, InstanceType, IDCInfo, OSType, \
    EndUser, Cluster, BusinessUnit, RuntimeEnvironment, Machine, Vm


class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields = ('url', 'id', 'name', 'desc')


class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('url', 'id', 'tag', 'cpu', 'memory', 'disk_ssd', 'disk_sas',
                  'disk_sata', 'nic', 'psu', 'raid_card', 'desc')


class InstanceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstanceType
        fields = ('url', 'id', 'tag', 'cpu', 'memory', 'desc')


class IDCInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IDCInfo
        fields = ('url', 'id', 'tag', 'name', 'location', 'desc')


class OSTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OSType
        fields = ('url', 'id', 'tag', 'desc')


class EndUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EndUser
        fields = ('url', 'id', 'username', 'fullname', 'department')


class ClusterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cluster
        fields = ('url', 'id', 'name', 'desc')


class BusinessUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = ('url', 'id', 'name', 'desc')


class RuntimeEnvironmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RuntimeEnvironment
        fields = ('url', 'id', 'name', 'desc')