from rest_framework.test import APITestCase
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from apps.users.models import User


class UserIndexViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='artem', password='1234', first_name='Artem')

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_404_when_no_token_provided(self):
        self.client.credentials()
        response = self.client.get('/users')

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_200_when_token_provided(self):
        response = self.client.get('/users')

        self.assertEqual(response.status_code, HTTP_200_OK)
