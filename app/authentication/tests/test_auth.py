from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class AuthAPITests(APITestCase):
    """
    Тесты для /auth/login и /auth/signup API.

    Methods:
    - test_login_valid_credentials(): Проверяет вход с верными учетными данными.
    - test_login_invalid_credentials(): Проверяет вход с неверными учетными данными.
    - test_signup_valid_data(): Проверяет успешную регистрацию пользователя с корректными данными.
    - test_signup_invalid_data(): Проверяет неуспешную регистрацию пользователя с некорректными данными.
    """

    def test_login_valid_credentials(self):
        """
        Проверяет вход с верными учетными данными.

        Создает пользователя, отправляет запрос на вход с верными данными и проверяет успешность входа.
        """
        user = User.objects.create_user(email='test@example.com',
                                        first_name='Test', last_name='User',
                                        password='testpassword')
        url = reverse('login')
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """
        Проверяет вход с неверными учетными данными.

        Создает пользователя, отправляет запрос на вход с неверными данными и проверяет ошибку входа.
        """
        User.objects.create_user(email='test@example.com', first_name='Test',
                                 last_name='User', password='testpassword')
        url = reverse('login')
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_signup_valid_data(self):
        """
        Проверяет успешную регистрацию пользователя с корректными данными.

        Отправляет запрос на регистрацию с корректными данными пользователя и проверяет успешность регистрации.
        """
        url = reverse('signup')
        data = {'email': 'newuser@example.com', 'first_name': 'New',
                'last_name': 'User', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_signup_invalid_data(self):
        """
        Проверяет неуспешную регистрацию пользователя с некорректными данными.

        Отправляет запрос на регистрацию с некорректными данными пользователя и проверяет ошибку регистрации.
        """
        url = reverse('signup')
        data = {'email': '', 'first_name': 'New', 'last_name': 'User',
                'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
