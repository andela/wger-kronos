import os
import logging
import tempfile
from io import StringIO
from django.core.management import call_command
from .base_testcase import WorkoutManagerTestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.conf import settings
from django.core.urlresolvers import reverse
from wger.core.models import UserProfile


class CreateUserCommand(WorkoutManagerTestCase):

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
        self.out = StringIO()
        User.objects.create(username='ManuelDominic',
                            email='manuel@andela.com', password='********')

    def test_access_api_user_creation(self):
        user = User.objects.get(username='ManuelDominic')
        profile = UserProfile.objects.get(user=user)
        profile.is_allowed = False
        Token.objects.create(key='group', user=user)
        call_command('add-user-rest-api', 'group', 'test', stdout=self.out)
        self.assertIn('Access granted to create api users', self.out.getvalue())
        call_command('add-user-rest-api', 'group', 'test', stdout=self.out)
        self.assertIn('User already has access to create other users', self.out.getvalue())

    def test_invalid_access_api_user_creation(self):
        user = User.objects.get(username='ManuelDominic')
        Token.objects.create(key='group', user=user)
        call_command('add-user-rest-api', 'anorld', 'anorld', stdout=self.out)
        self.assertIn('Invalid access, try again', self.out.getvalue())

    def test_access_get_api_users(self):
        User.objects.get(username='ManuelDominic')
        call_command('list-user-rest-api', 'fred', stdout=self.out)
        self.assertIn('USER', self.out.getvalue())
        self.assertIn('CREATED_BY', self.out.getvalue())

    def test_invalid_access_get_api_users(self):
        User.objects.get(username='ManuelDominic')
        call_command('list-user-rest-api', 'anorld', stdout=self.out)
        self.assertIn('username not found', self.out.getvalue())

    def test_post_valid_api_user_creation(self):
        user = User.objects.get(username='ManuelDominic')
        UserProfile.objects.filter(user=user).update(is_allowed=True)
        Token.objects.create(key='group', user=user)
        response = self.client.post(reverse('api_user'),
                                    {'api_key': 'group', 'username': 'Mandominic',
                                     'email': 'mandominic@gmail.com',
                                     'password': 'Mandominic123'})
        message = {"message": "api user successfully registered"}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, message)

    def test_post_not_allowed_api_user_creation(self):
        user = User.objects.get(username='ManuelDominic')
        UserProfile.objects.filter(user=user).update(is_allowed=False)
        Token.objects.create(key='group', user=user)
        response = self.client.post(reverse('api_user'),
                                    {'api_key': 'group', 'username': 'Mandominic',
                                     'email': 'mandominic@gmail.com',
                                     'password': 'Mandominic123'})
        message = "You're not allowed to create other users"
        self.assertEqual(response.status_code, 400)
        self.assertIn(message, response.data)
