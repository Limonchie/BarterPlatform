from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile



class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            password='Testpass123'
        )

    # регистрация
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, 'Регистрация')

    def test_register_view_post_success(self):
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('ad_list'))
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
        self.assertEqual(Profile.objects.filter(user__username='newuser').count(), 1)

    def test_register_view_post_invalid(self):
        data = {
            'username': 'newuser',
            'password1': '123',
            'password2': '123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'This password is too short.')

    # вход
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_success(self):
        data = {
            'username': 'testuser',
            'password': 'Testpass123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('ad_list'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_view_post_invalid(self):
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверное имя пользователя или пароль')


    def tearDown(self):
        self.test_user.delete()