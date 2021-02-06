from unittest import TestCase

from netguru.utils import create_hash, create_password


class UtilsTestCase(TestCase):

    def test_create_hash_length(self):
        some_hash = create_hash()
        self.assertEqual(len(some_hash), 32)

    def test_create_password_length(self):
        some_password = create_password()
        self.assertEqual(len(some_password), 8)

