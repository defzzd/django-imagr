# -*- coding: utf-8 -*-
from django.test import TestCase, Client, RequestFactory
from imagr_app.models import Photo, Album, ImagrUser

# Thanks to Brandon at:
#  http://stackoverflow.com/questions/15073227/django-unit-test-simple-example
# for getting the tests started

# Create your tests here.


class ClientUsesImagr(TestCase):
    fixtures = ['imagr_app_testdata.json']

    def setUp(self):
        self.client = Client()

    def test_empty_datas(self):
        self.client.login(username='', password='')
