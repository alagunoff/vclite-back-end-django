import json
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from apps.posts.models import Post
from apps.users.models import User
from apps.authors.models import Author
from apps.categories.models import Category
from apps.tags.models import Tag


class IndexViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        artem = User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')
        author = Author.objects.create(description='best', user=artem)
        category = Category.objects.create(category='sports')
        tag = Tag.objects.create(tag='2022')
        post = Post.objects.create(
            title='post', content='post', author=author, category=category)
        post.tags.add(tag)

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        response = self.client.get('/posts')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_method_correct_posts_number(self):
        response = self.client.get('/posts')

        self.assertEqual(response.data['count'], 1)

    def test_post_method_with_201_response(self):
        first_category_id = Category.objects.first().id
        first_tag_id = Tag.objects.first().id
        response = self.client.post(
            '/posts', json.dumps({'title': 'post', 'content': 'post', 'category_id': first_category_id, 'tags_ids': [first_tag_id]}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_post_method_with_401_response(self):
        self.client.credentials()
        first_category_id = Category.objects.first().id
        first_tag_id = Tag.objects.first().id
        response = self.client.post(
            '/posts', json.dumps({'title': 'post', 'content': 'post', 'category_id': first_category_id, 'tags_ids': [first_tag_id]}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class DetailViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        artem = User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')
        author = Author.objects.create(description='best', user=artem)
        category = Category.objects.create(category='sports')
        tag = Tag.objects.create(tag='2022')
        post = Post.objects.create(
            title='post', content='post', author=author, category=category)
        post.tags.add(tag)

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        first_post_id = Post.objects.first().id
        response = self.client.get(f'/posts/{first_post_id}')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_method_with_404_response(self):
        response = self.client.get('/posts/100500')

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_delete_method_with_401_response(self):
        self.client.credentials()
        first_post_id = Post.objects.first().id
        response = self.client.delete(f'/posts/{first_post_id}')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_delete_method_with_204_response(self):
        first_post_id = Post.objects.first().id
        response = self.client.delete(f'/posts/{first_post_id}')

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
