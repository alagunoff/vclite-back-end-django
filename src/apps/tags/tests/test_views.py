import json
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from apps.tags.models import Tag
from apps.users.models import User


class IndexViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(tag='2022')
        User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        response = self.client.get('/tags')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_post_method_with_201_response(self):
        response = self.client.post(
            '/tags', json.dumps({'tag': '2023'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_post_method_with_400_response(self):
        response = self.client.post(
            '/tags', json.dumps({'tag': '2022'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_post_method_with_401_response(self):
        self.client.credentials()
        response = self.client.post(
            '/tags', json.dumps({'tag': '2023'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class DetailViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(tag='2022')
        User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        tag_2022_id = Tag.objects.get(tag='2022').id
        response = self.client.get(f'/tags/{tag_2022_id}')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_put_method_with_200_response(self):
        tag_2022_id = Tag.objects.get(tag='2022').id
        response = self.client.put(
            f'/tags/{tag_2022_id}', json.dumps({'tag': '2023'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_delete_method_with_204_response(self):
        tag_2022_id = Tag.objects.get(tag='2022').id
        response = self.client.delete(f'/tags/{tag_2022_id}')

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
