import json
from rest_framework.test import APITestCase
from rest_framework.status import \
    HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,\
    HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, \
    HTTP_405_METHOD_NOT_ALLOWED

from apps.users.models import User


class UserIndexViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='artem', password='1234', first_name='Artem')

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_404_when_no_token_provided(self):
        self.client.credentials()
        response = self.client.get('/users')

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_get_200_when_token_provided(self):
        response = self.client.get('/users')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_post_201(self):
        response = self.client.post(
            '/users', json.dumps({'username': 'ivan', 'password': '1234', 'first_name': 'Ivan'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_post_400_when_user_already_exists(self):
        response = self.client.post(
            '/users', json.dumps({'username': 'artem', 'password': '1234', 'first_name': 'Artem'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class UserDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')
        User.objects.create_user(
            username='ivan', password='1234', first_name='Ivan')

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_delete_404_when_there_is_no_user(self):
        response = self.client.delete('/users/100500')

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_delete_401_when_no_credentials_provided(self):
        self.client.credentials()
        ivan_id = User.objects.get(username='ivan').id
        response = self.client.delete(f'/users/{ivan_id}')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_delete_204(self):
        ivan_id = User.objects.get(username='ivan').id
        response = self.client.delete(f'/users/{ivan_id}')

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')

    def test_get_405(self):
        response = self.client.get('/users/login')

        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_400_with_invalid_credentials(self):
        response = self.client.post(
            '/users/login', json.dumps({'username': 'artem', 'password': '123'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_post_200_with_valid_credentials(self):
        response = self.client.post(
            '/users/login', json.dumps({'username': 'artem', 'password': '1234'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_200_OK)
