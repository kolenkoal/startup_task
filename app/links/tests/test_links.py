from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.models import User
from links.models import Link


class LinkAPITests(APITestCase):
    """
    Тесты для LinkCreateAPIView и RedirectLinkAPIView.

    Methods:
    - test_create_link(): Проверяет создание новой ссылки.
    - test_redirect_valid_link(): Проверяет перенаправление по существующей ссылке.
    - test_redirect_invalid_link(): Проверяет обработку отсутствующей ссылки.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Alexander',
            last_name='Knyazhev'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_create_link(self):
        """
        Проверяет создание новой ссылки.

        Отправляет запрос на создание ссылки и проверяет успешный статус ответа.
        """
        url = reverse('create_link')
        data = {'url': 'http://example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_redirect_valid_link(self):
        """
        Проверяет перенаправление по существующей ссылке.

        Создает ссылку, отправляет запрос на перенаправление по этой ссылке и проверяет успешность перенаправления.
        """
        link = Link.objects.create(id='testid', user=self.user,
                                   url='http://example.com')
        url = reverse('redirect-link', args=['testid'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_redirect_invalid_link(self):
        """
        Проверяет обработку отсутствующей ссылки.

        Отправляет запрос на перенаправление по несуществующей ссылке и проверяет ответ "404 Not Found".
        """
        url = reverse('redirect-link', args=['invalidid'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
