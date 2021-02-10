import datetime
from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now

from netguru.utils import create_hash, create_password
from transfer.models import Transfer, UserAgent


class UtilsTestCase(TestCase):

    def test_create_hash_length(self):
        some_hash = create_hash()
        self.assertEqual(len(some_hash), 32)

    def test_create_password_length(self):
        some_password = create_password()
        self.assertEqual(len(some_password), 8)


class TransferModelTestCase(TestCase):

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
        self.assertEquals(f'/transfer/{transfer.url_hash}/', transfer.get_absolute_url())

    def test_get_password_url(self):
        """Check if get_password_url return correct value"""
        transfer = Transfer.objects.get(website="www.test_valid.com")
        self.assertEquals(
            f'{settings.DOMAIN}/transfer/password/{transfer.url_hash}', transfer.get_password_url()
        )

    def test_picture_url(self):
        """Check if get_picture_url return correct value"""
        transfer = Transfer.objects.get(website="www.test_valid.com")
        self.assertEquals(
            f'{settings.DOMAIN}/media/', transfer.get_picture_url(),
        )

    def test_get_api_url(self):
        """Check if get_api_url return correct value"""
        transfer = Transfer.objects.get(website="www.test_valid.com")
        self.assertEquals(
            f'{settings.DOMAIN}/api/download/{transfer.url_hash}', transfer.get_api_url()
        )

    def test_update_counter(self):
        """Check if counter incrementation is working properly"""
        transfer = Transfer.objects.get(website="www.test_valid.com")
        counter = randint(1, 10)
        for i in range(counter):
            transfer.update_counter()
        self.assertEquals(counter, transfer.correct_password_counter)


class TransferRequestsTestCase(TestCase):

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        User = get_user_model()
        User.objects.create_user('net', 'netguru@gmail.com', 'guru')
        Transfer.objects.create(website="http://www.netguru.com")

    def test_redirected_from_transfer_create_when_not_logged_in(self):
        response = self.client.get(reverse('transfer-create'))
        self.assertRedirects(response, '/accounts/login/?next=/transfer/create/')

    def test_no_redirected_from_transfer_password_when_incorrect_password(self):
        transfer_in = Transfer.objects.first()
        self.client.post(reverse('transfer-password', kwargs={'url_hash': transfer_in.url_hash}),
                                    {'password': 'wrong_password'})
        transfer_out = Transfer.objects.first()
        self.assertEquals(transfer_out.correct_password_counter, 0)

    def test_redirected_from_transfer_password_when_correct_password(self):
        transfer_in = Transfer.objects.first()
        response = self.client.post(reverse('transfer-password', kwargs={'url_hash': transfer_in.url_hash}),
                                    {'password': transfer_in.url_password})
        self.assertRedirects(response, 'http://www.netguru.com')
        transfer_out = Transfer.objects.first()
        self.assertEquals(transfer_out.correct_password_counter, 1)

    def test_create_by_view(self):
        self.client.login(username='net', password='guru')
        response = self.client.post(reverse('transfer-create'),
                                    {'website': 'http://www.google.com'})
        self.assertEquals(Transfer.objects.all().count(), 2)
        transfer = Transfer.objects.last()
        self.assertRedirects(response, f'/transfer/{transfer.url_hash}/')

    def test_detail_view_not_logged_in(self):
        transfer = Transfer.objects.first()
        response = self.client.get(reverse('transfer-detail', kwargs={'url_hash': transfer.url_hash}))
        self.assertRedirects(response, f'/accounts/login/?next=/transfer/{transfer.url_hash}/')

    def test_detail_view_logged_in(self):
        self.client.login(username='net', password='guru')
        self.client.post(reverse('transfer-create'),
                         {'website': 'http://www.google.com'})
        transfer = Transfer.objects.last()
        response = self.client.get(reverse('transfer-detail', kwargs={'url_hash': transfer.url_hash}))
        self.assertEquals(response.status_code, 200)

    def test_detail_view_logged_in_cannot_see_others_transfers(self):
        self.client.login(username='net', password='guru')
        transfer = Transfer.objects.last()
        response = self.client.get(reverse('transfer-detail', kwargs={'url_hash': transfer.url_hash}))
        self.assertEquals(response.status_code, 404)

    def test_download_view_proper_url(self):
        transfer = Transfer.objects.first()
        response = self.client.get(
            reverse('transfer-download', kwargs={'url_hash': transfer.url_hash, 'url_password': transfer.url_password}))
        self.assertEquals(response.status_code, 200)

    def test_download_view_wrong_url(self):
        response = self.client.get(
            reverse('transfer-download', kwargs={'url_hash': 'wrong_hash', 'url_password': 'wrong_password'}))
        self.assertEquals(response.status_code, 404)

    def test_user_agent(self):
        self.client.login(username='net', password='guru')
        transfer = Transfer.objects.last()
        response = self.client.get(reverse('transfer-detail', kwargs={'url_hash': transfer.url_hash}))
        self.assertEquals(response.status_code, 404)
        user_agent = UserAgent.objects.first()
        self.assertEquals(user_agent.user.username, 'net')
        self.assertEquals(user_agent.user_agent, 'Mozilla/5.0')
