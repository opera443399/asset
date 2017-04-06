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
        self.default_test_url = '/api/v1/vendors/'
        self.default_test_data = {'name': 'tttt_01', 'desc': 'tttt_02'}
        self.default_test_data_err = {'name': 'tttt_01_length_over_20', 'desc': 'tttt_02'}
        self.default_model = Vendor

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'tttt_01_u', 'desc': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeviceTypeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()
        self.default_test_url = '/api/v1/models/'
        self.default_test_data = {'tag': 'tttt_01', 'desc': 'tttt_02'}
        self.default_test_data_err = {'tag': 'tttt_01_length_over_10', 'desc': 'tttt_02'}
        self.default_model = DeviceType

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'tag': 'tttt_01_u', 'desc': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'tag': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class InstanceTypeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()
        self.default_test_url = '/api/v1/offerings/'
        self.default_test_data = {'tag': 'tttt_01', 'desc': 'tttt_02'}
        self.default_test_data_err = {'tag': 'tttt_01_length_over_10', 'desc': 'tttt_02'}
        self.default_model = InstanceType

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'tag': 'tttt_01_u', 'desc': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'tag': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class IDCInfoTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()
        self.default_test_url = '/api/v1/idcs/'
        self.default_test_data = {'tag': 'tttt_01', 'desc': 'tttt_02'}
        self.default_test_data_err = {'tag': 'tttt_01_length_over_10', 'desc': 'tttt_02'}
        self.default_model = IDCInfo

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'tag': 'tttt_01_u', 'desc': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'tag': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OSTypeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()
        self.default_test_url = '/api/v1/os/'
        self.default_test_data = {'tag': 'tttt_01', 'desc': 'tttt_02'}
        self.default_test_data_err = {'tag': 'tttt_01_length_over_20', 'desc': 'tttt_02'}
        self.default_model = OSType

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'tag': 'tttt_01_u', 'desc': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'tag': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().tag, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EndUserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()
        self.default_test_url = '/api/v1/endusers/'
        self.default_test_data = {'username': 'tttt_01', 'department': 'tttt_02'}
        self.default_test_data_err = {'username': 'tttt_01_length_over_20', 'department': 'tttt_02'}
        self.default_model = EndUser

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().username, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().username, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().department, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'username': 'tttt_01_u', 'department': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().username, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().department, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'username': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().username, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().department, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ClusterTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()
        self.default_test_url = '/api/v1/clusters/'
        self.default_test_data = {'name': 'tttt_01', 'desc': 'tttt_02'}
        self.default_test_data_err = {'name': 'tttt_01_length_over_20', 'desc': 'tttt_02'}
        self.default_model = Cluster

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'tttt_01_u', 'desc': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BusinessUnitTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()
        self.default_test_url = '/api/v1/bizunits/'
        self.default_test_data = {'name': 'tttt_01', 'desc': 'tttt_02'}
        self.default_test_data_err = {'name': 'tttt_01_length_over_20', 'desc': 'tttt_02'}
        self.default_model = BusinessUnit

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'tttt_01_u', 'desc': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RuntimeEnvironmentTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('t01', email='t01@test.com', password='t01t02t03')
        self.user.save()
        self.default_test_url = '/api/v1/env/'
        self.default_test_data = {'name': 'tttt_01', 'desc': 'tttt_02'}
        self.default_test_data_err = {'name': 'tttt_01_length_over_20', 'desc': 'tttt_02'}
        self.default_model = RuntimeEnvironment

    def log_in(self):
        self.client.login(username='t01', password='t01t02t03')

    def test_create_api_without_auth(self):
        """
        Ensure we can create a new object without auth.
        """
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_err_field_length_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        but with a situation: len(some_field) > max_allowed_characters
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data_err
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_api_with_auth(self):
        """
        Ensure we can create a new object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01')

    def test_list_api_with_auth(self):
        """
        Ensure we can list the objects with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)

    def test_retrieve_api_with_auth(self):
        """
        Ensure we can retrieve a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_update_api_with_auth(self):
        """
        Ensure we can update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'tttt_01_u', 'desc': 'tttt_02_u'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02_u')

    def test_patch_api_with_auth(self):
        """
        Ensure we can partial update a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        data = {'name': 'tttt_01_u'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.default_model.objects.count(), 1)
        self.assertEqual(self.default_model.objects.get().name, 'tttt_01_u')
        self.assertEqual(self.default_model.objects.get().desc, 'tttt_02')

    def test_destroy_api_with_auth(self):
        """
        Ensure we can destroy a object with auth.
        """
        self.log_in()
        url = self.default_test_url
        data = self.default_test_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        response_content = json.loads(response.content.decode('utf-8'))
        result = response_content['results'][0]

        url = result['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
