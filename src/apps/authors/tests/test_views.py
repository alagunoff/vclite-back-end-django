import json
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from apps.authors.models import Author
from apps.users.models import User


class IndexViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username='ivan', password='1234', first_name='Ivan')

        artem = User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')
        Author.objects.create(description='best', user=artem)

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        response = self.client.get('/authors')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_method_with_401_response(self):
        self.client.credentials()
        response = self.client.get('/authors')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_post_method_with_201_response(self):
        ivan_id = User.objects.get(username='ivan').id
        response = self.client.post(
            '/authors', json.dumps({'description': 'best', 'user_id': ivan_id}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_post_method_with_401_response(self):
        self.client.credentials()
        artem_id = User.objects.get(username='artem').id
        response = self.client.post(
            '/authors', json.dumps({'description': 'best', 'user_id': artem_id}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class DetailViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username='ivan', password='1234', first_name='Ivan')

        artem = User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')
        Author.objects.create(description='best', user=artem)

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        first_author_id = Author.objects.first().id
        response = self.client.get(f'/authors/{first_author_id}')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_method_with_401_response(self):
        self.client.credentials()
        first_author_id = Author.objects.first().id
        response = self.client.get(f'/authors/{first_author_id}')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_delete_method_with_204_response(self):
        first_author_id = Author.objects.first().id
        response = self.client.delete(f'/authors/{first_author_id}')

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_delete_method_with_401_response(self):
        self.client.credentials()
        first_author_id = Author.objects.first().id
        response = self.client.delete(f'/authors/{first_author_id}')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
