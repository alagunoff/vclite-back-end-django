from rest_framework.test import APITestCase

from apps.categories.models import Category


class TagModelTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(category='sports')

    def test_str(self):
        first_category = Category.objects.first()

        self.assertEqual(str(first_category), first_category.category)

    def test_category_max_length(self):
        first_category = Category.objects.first()

        self.assertEqual(first_category._meta.get_field(
            'category').max_length, 70)
