import json
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from apps.comments.models import Comment
from apps.users.models import User
from apps.authors.models import Author
from apps.categories.models import Category
from apps.tags.models import Tag
from apps.posts.models import Post


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
        Comment.objects.create(comment='I liked it very much', post=post)
        Comment.objects.create(comment='I hate it very much', post=post)

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {User.objects.get(username="artem").auth_token.key}')

    def test_get_method_with_200_response(self):
        first_post_id = Post.objects.first().id
        response = self.client.get(f'/posts/{first_post_id}/comments')

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_method_correct_comments_number(self):
        first_post_id = Post.objects.first().id
        response = self.client.get(f'/posts/{first_post_id}/comments')

        self.assertEqual(response.data['count'], 2)

    def test_post_method_with_201_response(self):
        first_post_id = Post.objects.first().id
        response = self.client.post(
            f'/posts/{first_post_id}/comments', json.dumps({'comment': 'I do not care about this post'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_post_method_with_401_response(self):
        self.client.credentials()
        first_post_id = Post.objects.first().id
        response = self.client.post(
            f'/posts/{first_post_id}/comments', json.dumps({'comment': 'I do not care about this post'}), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
