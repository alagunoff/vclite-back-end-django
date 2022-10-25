import json
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from apps.categories.models import Category
from apps.users.models import User


class IndexViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(category='sports')
        User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        response = self.client.get('/categories')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_post_method_with_201_response(self):
        response = self.client.post(
            '/categories', json.dumps({'category': 'cooking'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_post_method_with_401_response(self):
        self.client.credentials()
        response = self.client.post(
            '/categories', json.dumps({'category': 'cooking'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class DetailViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(category='sports')
        User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        first_category_id = Category.objects.first().id
        response = self.client.get(f'/categories/{first_category_id}')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_put_method_with_200_response(self):
        first_category_id = Category.objects.first().id
        response = self.client.put(
            f'/categories/{first_category_id}', json.dumps({'category': 'cooking'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_delete_method_with_204_response(self):
        first_category_id = Category.objects.first().id
        response = self.client.delete(f'/categories/{first_category_id}')

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_delete_method_with_401_response(self):
        self.client.credentials()
        first_category_id = Category.objects.first().id
        response = self.client.delete(f'/categories/{first_category_id}')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
