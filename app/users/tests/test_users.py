from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from users.models import User


class UserLinksAPIViewTestCase(TestCase):
    """
    Тесты для API-представления UserLinksAPIView.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            first_name='John', last_name='Doe', email='test@example.com',
            password='password'
        )

    def test_authenticated_user_access(self):
        """
        Тестирует доступ аутентифицированного пользователя к представлению.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('user-links')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_access(self):
        """
        Тестирует доступ к представлению без аутентификации.
        """
        url = reverse('user-links')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
