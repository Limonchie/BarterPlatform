from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad

class AdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Item',
            description='Test Description',
            category='electronics',
            condition='new'
        )

    def test_ad_creation(self):
        self.assertEqual(self.ad.title, 'Test Item')
        self.assertEqual(self.ad.user.username, 'testuser')