# coding=utf-8
# ----------------------------------
# @ 2017/4/6
# @ PC
# ----------------------------------

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Vendor, DeviceType, InstanceType, IDCInfo, OSType, \
    EndUser, Cluster, BusinessUnit, RuntimeEnvironment, Machine, Vm


# Create your tests here.
# ================================ MODELS ================================
class MachineMethodTests(TestCase):
    def test_was_added_recently_with_future_word(self):
        """
        was_added_recently() should return False for machine added in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_machine = Machine(dt_created=time)
        self.assertEqual(future_machine.was_added_recently(), False)

    def test_was_added_recently_with_old_word(self):
        """
        was_added_recently() should return False for machine added in the past.
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_machine = Machine(dt_created=time)
        self.assertEqual(old_machine.was_added_recently(), False)

    def test_was_added_recently_with_recent_word(self):
        """
        was_added_recently() should return True for machine added recently.
        """
        time = timezone.now() - datetime.timedelta(hours=5)
        recent_machine = Machine(dt_created=time)
        self.assertEqual(recent_machine.was_added_recently(), True)


class VmMethodTests(TestCase):
    def test_was_added_recently_with_future_word(self):
        """
        was_added_recently() should return False for machine added in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_vm = Vm(dt_created=time)
        self.assertEqual(future_vm.was_added_recently(), False)

    def test_was_added_recently_with_old_word(self):
        """
        was_added_recently() should return False for machine added in the past.
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_vm = Vm(dt_created=time)
        self.assertEqual(old_vm.was_added_recently(), False)

    def test_was_added_recently_with_recent_word(self):
        """
        was_added_recently() should return True for machine added recently.
        """
        time = timezone.now() - datetime.timedelta(hours=5)
        recent_vm = Vm(dt_created=time)
        self.assertEqual(recent_vm.was_added_recently(), True)


# ================================ VIEWS ================================
class NormalViewTests(TestCase):
    def test_show_index_view(self):
        """
        show_index
        """
        response = self.client.get(reverse('assets:show_index'))
        self.assertEqual(response.status_code, 200)

    def test_show_about_view(self):
        """
        show_about
        """
        response = self.client.get(reverse('assets:show_about'))
        self.assertEqual(response.status_code, 200)

    def test_import_hosts_view(self):
        """
        import_hosts
        """
        response = self.client.get(reverse('assets:import_hosts'))
        self.assertEqual(response.status_code, 302)

    def test_import_vms_view(self):
        """
        import_vms
        """
        response = self.client.get(reverse('assets:import_vms'))
        self.assertEqual(response.status_code, 302)

    def test_list_hosts_view(self):
        """
        list_hosts
        """
        response = self.client.get(reverse('assets:list_hosts'))
        self.assertEqual(response.status_code, 302)

    def test_list_vms_view(self):
        """
        list_vms
        """
        response = self.client.get(reverse('assets:list_vms'))
        self.assertEqual(response.status_code, 302)


# ================================ VIEWS API ================================
class VendorTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_vendor_api_without_auth(self):
        """
        Ensure we can create a new vendor object without auth.
        """
        url = '/api/v1/vendors/'
        data = {'name': 'test_vendor_01', 'desc': 'test_vendor_01_desc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_vendor_api_with_auth(self):
        """
        Ensure we can create a new vendor object with auth.
        """
        self.log_in()
        url = '/api/v1/vendors/'
        data = {'name': 'test_vendor_01', 'desc': 'test_vendor_01_desc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'test_vendor_01')

    def test_list_vendors_api_with_auth(self):
        """
        Ensure we can list the vendors object with auth.
        """
        self.log_in()
        url = '/api/v1/vendors/'
        data = {'name': 'test_vendor_02', 'desc': 'test_vendor_02_desc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/v1/vendors/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_retrieve_vendor_api_with_auth(self):
        """
        Ensure we can retrieve a vendor object with auth.
        """
        self.log_in()
        url = '/api/v1/vendors/'
        data = {'name': 'test_vendor_03', 'desc': 'test_vendor_03_desc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/v1/vendors/'
        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'test_vendor_03')

    def test_update_vendor_api_with_auth(self):
        """
        Ensure we can update a vendor object with auth.
        """
        self.log_in()
        url = '/api/v1/vendors/'
        data = {'name': 'test_vendor_04', 'desc': 'test_vendor_04_desc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/v1/vendors/'
        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'test_vendor_04_u', 'desc': 'test_vendor_04_desc_updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'test_vendor_04_u')

    def test_destroy_vendor_api_with_auth(self):
        """
        Ensure we can destroy a vendor object with auth.
        """
        self.log_in()
        url = '/api/v1/vendors/'
        data = {'name': 'test_vendor_05', 'desc': 'test_vendor_05_desc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/v1/vendors/'
        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
