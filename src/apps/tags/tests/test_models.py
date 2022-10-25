from rest_framework.test import APITestCase

from apps.tags.models import Tag


class TagModelTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(tag='2022')

    def test_str(self):
        tag = Tag.objects.get(tag='2022')

        self.assertEqual(str(tag), tag.tag)

    def test_tag_max_length(self):
        tag = Tag.objects.get(tag='2022')

        self.assertEqual(tag._meta.get_field('tag').max_length, 30)
