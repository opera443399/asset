# coding=utf-8
# ----------------------------------
# @ 2017/3/30
# @ PC
# ----------------------------------

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime

from .models import Machine, Vm


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