from rest_framework.test import APITestCase

from apps.authors.models import Author
from apps.users.models import User


class ModelTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        artem = User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')
        Author.objects.create(description='best', user=artem)

    def test_str(self):
        first_author = Author.objects.first()

        self.assertEqual(str(first_author), first_author.user.username)

    def test_description_max_length(self):
        first_author = Author.objects.first()

        self.assertEqual(first_author._meta.get_field(
            'description').max_length, 255)
