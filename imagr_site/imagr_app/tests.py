# -*- coding: utf-8 -*-
import unittest
from django.test import TestCase, SimpleTestCase, TransactionTestCase
from django.test import Client, RequestFactory
from imagr_app.models import Photo, Album, ImagrUser
from django.test.utils import setup_test_environment, teardown_test_environment

# This workaround suggested by dghubble at:
# http://stackoverflow.com/questions/17912060/django-test-client-always-returning-301
# when 301 errors are being returned on pages that re-direct to SSL pages
# from django.test.utils import override_settings

# Thanks to Brandon at:
#  http://stackoverflow.com/questions/15073227/django-unit-test-simple-example
# for getting the tests started

# Create your tests here.


class testImagrTestCase(TestCase):
    fixtures = ['imagr_app_testdata.json']

    def setUp(self):
        self.client = Client()

    def test_empty_datas(self):
        self.client.login(username='', password='')


# TransactionTestCase's need:
#  from django.test import TransactionTestCase
class testImagrTransactionTestCase(TransactionTestCase):
    fixtures = ['imagr_app_testdata.json']

    def test_accessRestrictedURLS(self):
        response = self.client.post('/accounts/login/', {
            'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        # print response

        response = self.client.get('/imagr_app/album/1/')
        self.assertEqual(response.status_code, 200)
        # print response

        response = self.client.get('/imagr_app/photo/8/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/imagr_app/photo/9/')
        self.assertEqual(response.status_code, 404)


# SimpleTestCase's need:
#  from django.test import SimpleTestCase

# The override decorator was suggested as a fix to unknown 301 status codes
# @override_settings(SSLIFY_DISABLE=True)
class testImagrSimpleTestCase(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_accessURLS(self):

        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/imagr_app/')
        self.assertEqual(response.status_code, 200)


# These test cases should be simple enough to require no Django
class testImagrunittestTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    setup_test_environment()
    unittest.main()
    teardown_test_environment()
