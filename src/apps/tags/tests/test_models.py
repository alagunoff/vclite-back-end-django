from rest_framework.test import APITestCase

from apps.tags.models import Tag


class TagModelTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(tag='2022')

    def test_str(self):
        first_tag = Tag.objects.first()

        self.assertEqual(str(first_tag), first_tag.tag)

    def test_tag_max_length(self):
        first_tag = Tag.objects.first()

        self.assertEqual(first_tag._meta.get_field('tag').max_length, 30)
