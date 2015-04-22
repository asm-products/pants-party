from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient

from .models import Subscription
from ppuser.models import CustomUser


class FAQTestCase(TestCase):
    def setUp(self):
        self.creation_date = timezone.now()
        self.subscription1 = Subscription.objects.create(email='user1@example.com')
        self.subscription2 = Subscription.objects.create(email='user2@example.com')
        self.subscription3 = Subscription.objects.create(email='user3@example.com')

    def test_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            Subscription.objects.create(email='user1@example.com')

    def test_subscription_via_api(self):
        client = APIClient()
        response = client.get('/api/subscription/')
        self.assertEquals(response.status_code, 405)

        data1 = {'email': 'user1@example.com'}
        data2 = {'email': 'user4@example.com'}

        response = client.post('/api/subscription/', data1)
        # Must raise 409 due to use of already-existing email
        self.assertEquals(response.status_code, 409)
        response = client.post('/api/subscription/', data2)
        # Must return 201 for created instance
        self.assertEquals(response.status_code, 201)
