from rest_framework.test import APITestCase

from apps.posts.models import Post
from apps.posts.constants import DEFAULT_POST_BASE64_IMAGE
from apps.users.models import User
from apps.authors.models import Author
from apps.categories.models import Category
from apps.tags.models import Tag


class ModelTestCase(APITestCase):
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

    def test_str(self):
        first_post = Post.objects.first()

        self.assertEqual(str(first_post), first_post.title)

    def test_title_max_length(self):
        first_post = Post.objects.first()

        self.assertEqual(first_post._meta.get_field('title').max_length, 30)

    def test_content_max_length(self):
        first_post = Post.objects.first()

        self.assertIsNone(first_post._meta.get_field('content').max_length)

    def test_image_default(self):
        first_post = Post.objects.first()

        self.assertEqual(first_post._meta.get_field(
            'image').default, DEFAULT_POST_BASE64_IMAGE)

    def test_image_max_length(self):
        first_post = Post.objects.first()

        self.assertEqual(first_post._meta.get_field(
            'image').max_length, 900000)

    def test_is_draft_default(self):
        first_post = Post.objects.first()

        self.assertFalse(first_post._meta.get_field('is_draft').default)
