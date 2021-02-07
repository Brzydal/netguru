import datetime
from random import randint

from django.conf import settings
from django.test import TestCase
from django.utils.timezone import now

from netguru.utils import create_hash, create_password
from transfer.models import Transfer


class UtilsTestCase(TestCase):

    def test_create_hash_length(self):
        some_hash = create_hash()
        self.assertEqual(len(some_hash), 32)

    def test_create_password_length(self):
        some_password = create_password()
        self.assertEqual(len(some_password), 8)


class TransferTestCase(TestCase):

    def setUp(self):
        two_days_ago = now() + datetime.timedelta(days=-2)
        Transfer.objects.create(website="www.test_valid.com")
        transfer_invalid = Transfer.objects.create(website="www.test_invalid.com")
        transfer_invalid.created = two_days_ago
        transfer_invalid.save()

    def test_transfer_is_valid(self):
        """Check when transfer is valid"""
        transfer = Transfer.objects.get(website="www.test_valid.com")
        self.assertTrue(transfer.is_valid())

    def test_transfer_is_invalid(self):
        """Check when transfer is invalid"""
        transfer = Transfer.objects.get(website="www.test_invalid.com")
        self.assertFalse(transfer.is_valid())

    def test_get_absolute_url(self):
        """Check if get_absolute_url return correct value"""
        transfer = Transfer.objects.get(website="www.test_valid.com")
        self.assertEquals(transfer.get_absolute_url(), f'/transfer/{transfer.url_hash}/')

    def test_get_password_url(self):
        """Check if get_password_url return correct value"""
        transfer = Transfer.objects.get(website="www.test_valid.com")
        self.assertEquals(
            transfer.get_password_url(), f'{settings.DOMAIN}/transfer/password/{transfer.url_hash}'
        )

    def test_update_counter(self):
        """Check if counter incrementation is working properly"""
        transfer = Transfer.objects.get(website="www.test_valid.com")
        counter = randint(1, 10)
        for i in range(counter):
            transfer.update_counter()
        self.assertEquals(transfer.correct_password_counter, counter)
