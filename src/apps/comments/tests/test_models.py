from rest_framework.test import APITestCase

from apps.comments.models import Comment
from apps.users.models import User
from apps.authors.models import Author
from apps.categories.models import Category
from apps.tags.models import Tag
from apps.posts.models import Post


class CommentModelTestCase(APITestCase):
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

    def test_str(self):
        first_comment = Comment.objects.first()

        self.assertEqual(str(first_comment),
                         f'{first_comment.comment[:10]}...')

    def test_comment_max_length(self):
        first_comment = Comment.objects.first()

        self.assertIsNone(first_comment._meta.get_field('comment').max_length)
