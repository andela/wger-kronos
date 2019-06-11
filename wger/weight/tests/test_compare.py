import os
import logging
import tempfile
from wger.core.tests.base_testcase import WorkoutManagerTestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.conf import settings
from django.core.urlresolvers import reverse
from wger.weight.models import WeightEntry


class WeightComparisonTestCase(WorkoutManagerTestCase):

    def setUp(self):
        self.client = APIClient()
        os.environ['RECAPTCHA_TESTING'] = 'True'
        if os.environ.get('TEST_MOBILE') == 'True':
            settings.FLAVOURS = ('mobile',)
            self.is_mobile = True

        # Set logging level
        logging.disable(logging.INFO)

        # Set MEDIA_ROOT
        self.media_root = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self.media_root
        User.objects.create(username='ManuelDominic',
                            email='manuel@andela.com', password='********')
        User.objects.create(username='Dominic',
                            email='dominic@andela.com', password='********')

    def test_get_weight_data_with_username(self):
        self.user_login()
        user1 = User.objects.get(username='ManuelDominic')
        WeightEntry.objects.create(user=user1, weight=64, date='2019-06-17')
        user2 = User.objects.get(username='Dominic')
        WeightEntry.objects.create(user=user2, weight=53, date='2019-06-17')
        response = self.client.get(
            reverse(
                'comparison_weight:weight-data-1',
                kwargs={
                    'username': user2.username}))
        self.assertIn('other', response.data[0])
        self.assertIn('weight', response.data[0]['other'])
        self.assertIn('date', response.data[0]['other'])

    def test_get_weight_data_user_with_no_weight(self):
        self.user_login()
        user = User.objects.get(username='Dominic')
        WeightEntry.objects.create(user=user, weight=53, date='2019-06-17')
        response = self.client.get(
            reverse(
                'comparison_weight:weight-data-1',
                kwargs={
                    'username': 'ManuelDominic'}))
        self.assertEqual([], response.data)
