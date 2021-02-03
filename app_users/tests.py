from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.urls import reverse
from .models import Profile

USER_LOGIN = 'jacob'
USER_PASSWORD = '123456'
USER_EMAIL = '123456@jacob.com'
USER_FIRST_NAME = 'Jacob'
USER_LAST_NAME = 'Smith'
USER_ABOUT = 'I am jacob'


class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=USER_LOGIN,
            email=USER_EMAIL,
            password=USER_PASSWORD,
            first_name=USER_FIRST_NAME,
            last_name=USER_LAST_NAME,
        )
        Profile.objects.create(user=self.user, about=USER_ABOUT)

    def test_login_exists_at_desired_location(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_authentication_user(self):
        url = reverse('login')
        response = self.client.post(url, {'username': USER_LOGIN, 'password': USER_PASSWORD}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, USER_LOGIN)

    def test_logout_exists_at_desired_location(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')

    def test_logout_user(self):
        self.client.login(username=USER_LOGIN, password=USER_PASSWORD)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['user'], AnonymousUser)

    def test_account_about_exists_at_desired_location(self):
        response = self.client.get(f'/user/account/{self.user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/account.html')

    def test_register_exists_at_desired_location(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_add_user_and_profile(self):
        url = reverse('register')
        from io import BytesIO
        file = BytesIO(b'data')
        response = self.client.post(url, {
            'about': 'test',
            'file_field': file,
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password1': 'test_pass',
            'password2': 'test_pass'
        }, follow=True)
        self.client.login(username='test', password='test_pass')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['user'].profile.photo)

    def test_account_edit_exists_at_desired_location(self):
        response = self.client.get(f'/user/account/{self.user.id}/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit.html')

    def test_account_edit_changes_info(self):
        from io import BytesIO
        file = BytesIO(b'data')
        self.client.login(username=USER_LOGIN, password=USER_PASSWORD)
        response = self.client.post(f'/user/account/{self.user.id}/edit/',
                                    {'first_name': 'test', 'last_name': 'test', 'about': 'test', 'file_field': file},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].profile.about, 'test')
        self.assertEqual(response.context['user'].first_name, 'test')
        self.assertEqual(response.context['user'].last_name, 'test')
        self.assertIsNotNone(response.context['user'].profile.photo)
